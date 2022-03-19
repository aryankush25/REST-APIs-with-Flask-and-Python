import sqlite3

connection = sqlite3.connect('data.sqlite')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id INT, username TEXT, password TEXT);'

cursor.execute(create_table)

user = (1, 'Aryan', 'test@123')
insert_query = "INSERT INTO users VALUES (?, ?, ?);"
cursor.execute(insert_query, user)

users = [
    (1, 'Kush', 'test@123'),
    (2, 'Rahul', 'test@123'),
    (3, 'Honey', 'test@123'),
]

cursor.executemany(insert_query, users)

select_query = 'SELECT * FROM users;'
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
