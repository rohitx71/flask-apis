from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store_model import StoreModel


class Store(Resource):
    TABLE_NAME = 'store'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

    @jwt_required()
    def put(self, name):
        item = StoreModel.find_by_name(name)
        if item is None:
            item = StoreModel(name)
        else:
            item['name'] = name
        item.save_to_db()
        return item.json()


class StoreList(Resource):

    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
