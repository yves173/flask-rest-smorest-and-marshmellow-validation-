import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores
from schemas import ItemSchema,ItemUpdateSchema



blp=Blueprint('items',__name__,description='Opreration on the Items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,'item can not be found!')


    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self,itemdata,item_id):

        try:
            item=items[item_id]
            item |=itemdata
            return item,201
        except KeyError:
            abort(404,'store can not be found!')

    def delete(self,item_id):
        try:
            del items[item_id]
            return {'message':f'item {item_id} is deleted'}
        except KeyError:
            abort(404,'store can not be found!')



@blp.route('/item')
class ItemList(MethodView):

    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return {'items':list(items.values())}

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,itemdata):

        if itemdata['store_id'] not in stores:
            abort(404,'store can not be found!')

        itemId=uuid.uuid4().hex
        newItem={**itemdata,'item_id':itemId}
        items[itemId]=newItem
        return newItem,201