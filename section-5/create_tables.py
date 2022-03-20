import sqlite3

connection = sqlite3.connect('section-5/data.sqlite')

cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);'

cursor.execute(create_table)

connection.commit()

connection.close()
