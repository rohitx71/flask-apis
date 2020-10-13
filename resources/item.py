from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    get_jwt_claims,
    fresh_jwt_required
)
from models.item_model import ItemModel

BLANK_ERROR = "'{}' cannot be blank."
ITEM_NOT_FOUND = 'Item not found'
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ADMIN_PRIVILEGE_REQUIRED = 'Admin privilege required'
ITEM_DELETED = 'Item deleted'
INSERTION_ERROR = "An error occurred inserting the item."
MORE_DATA_ON_LOGIN = "More data available if you log in."


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help=BLANK_ERROR.format("price")
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    @jwt_required
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": INSERTION_ERROR}
        return item.json()

    @classmethod
    @jwt_required
    def delete(cls, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': ADMIN_PRIVILEGE_REQUIRED}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': ITEM_DELETED}

    @classmethod
    @jwt_required
    def put(cls, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'

    @classmethod
    @jwt_optional
    def get(cls):
        user_id = get_jwt_claims()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items}
        return {'items': [item['name'] for item in items],
                'message': MORE_DATA_ON_LOGIN}
