import sqlite3
from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field can not be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        else:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(None, name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred while inserting item "}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        if ItemModel.find_by_name(name) is None:
            return {"message": f'An item with name {name} does not exists.'}, 400

        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?;'

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted.'}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        try:
            if item is None:
                item = ItemModel(None, name, data['price'])
                item.insert()
            else:
                item = ItemModel(item.id, name, data['price'])
                item.update()
        except:
            return {"message": "An error occurred while putting item "}, 500

        return item.json(), 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'select * from items;'

        result = cursor.execute(query)

        items = []

        for row in result:
            items.append(
                {"item": {'id': row[0], 'name': row[1], 'price': row[2]}}
            )

        connection.commit()
        connection.close()

        return {'items': items}, 200
