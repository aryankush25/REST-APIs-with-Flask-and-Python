import sqlite3


class ItemModel:
    def __init__(self,  id, name, price) -> None:
        self.id = id
        self.name = name
        self.price = price

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?;'

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (NULL, ?, ?);'
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?;'
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()