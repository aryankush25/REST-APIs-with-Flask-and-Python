import sqlite3

connection = sqlite3.connect('data.sqlite')

cursor = connection.cursor()

create_users_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT);'

cursor.execute(create_users_table)

create_items_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL);'

cursor.execute(create_items_table)

cursor.execute("INSERT INTO items VALUES (NULL, 'test', 10.78)")

connection.commit()

connection.close()
