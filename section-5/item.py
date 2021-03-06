import sqlite3
from flask_restful import Resource,  reqparse
from flask_jwt import jwt_required

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field can not be left blank")

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?;'

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {'id': row[0], 'name': row[1], 'price': row[2]}}

    @classmethod
    def insert_item(cls, name, price):
        item = {'name': name, 'price': price}

        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (NULL, ?, ?);'

        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if (item):
            return item, 200
        else:
            return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = self.insert_item(name, data['price'])

        return item, 201

    @jwt_required()
    def delete(self, name):
        if self.find_by_name(name) is None:
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

        item = self.find_by_name(name)
        if item is None:
            item = self.insert_item(name, data['price'])
        else:
            item = {'name': name, 'price': data['price']}

            connection = sqlite3.connect('data.sqlite')
            cursor = connection.cursor()

            query = 'UPDATE items SET price=? WHERE name=?;'

            cursor.execute(query, (item['price'], item['name']))
            connection.commit()
            connection.close()

        return item, 200


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
