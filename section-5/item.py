import sqlite3
from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field can not be left blank")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('section-5/data.sqlite')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?;'

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if (row):
            return {"item": {'id': row[0], 'name': row[1], 'price': row[2]}}, 200
        else:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {"message": f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted.'}, 200

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item, 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}, 200
