from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store_model import StoreModel

BLANK_ERROR = "'{}' cannot be blank."
STORE_NOT_FOUND = 'Store not found'
STORE_ALREADY_EXISTS = "A store with name '{}' already exists."
STORE_DELETED = 'Store deleted'
INSERTION_ERROR = "An error occurred inserting the item."


class Store(Resource):
    TABLE_NAME = 'store'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=float,
        required=True,
        help=BLANK_ERROR.format("name"),
    )

    @classmethod
    @jwt_required()
    def get(cls, name):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            return {'message': STORE_ALREADY_EXISTS.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": INSERTION_ERROR}, 500
        return store.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': STORE_DELETED}

    @classmethod
    @jwt_required()
    def put(cls, name):
        item = StoreModel.find_by_name(name)
        if item is None:
            item = StoreModel(name)
        else:
            item['name'] = name
        item.save_to_db()
        return item.json()


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {'stores': [x.json() for x in StoreModel.find_all()]}
