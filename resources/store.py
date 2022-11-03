import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema


blp=Blueprint('stores',__name__,description='Operations on the store')

@blp.route('/store/<string:store_id>')
class Store(MethodView):

    @blp.response(200,StoreSchema)
    def get(self,store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404,'store can not be found!')


    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def put(self,storedata,store_id):

        try:
            store=stores[store_id]
            store |=storedata
            return store,201
        except KeyError:
            abort(404,'store can not be found!')

    def delete(self,store_id):
        try:
            del stores[store_id]
            return {'message':f'store {store_id} is deleted'},201
        except KeyError:
            abort(404,'store can not be found!')

    
@blp.route('/store')
class StoreList(MethodView):

    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,storedata):

        storeID=uuid.uuid4().hex
        new_store={**storedata,'store_id':storeID}
        stores[storeID]=new_store
        return new_store,201