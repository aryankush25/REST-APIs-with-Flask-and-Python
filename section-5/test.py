import sqlite3

connection = sqlite3.connect('section-5/data.sqlite')

cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT);'

cursor.execute(create_table)

user = ('Aryan', 'test@123')
insert_query = "INSERT INTO users VALUES (NULL, ?, ?);"
cursor.execute(insert_query, user)

users = [
    ('Kush', 'test@123'),
    ('Rahul', 'test@123'),
    ('Honey', 'test@123'),
]

cursor.executemany(insert_query, users)

select_query = 'SELECT * FROM users;'
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
