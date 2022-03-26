from flask_restful import Resource, reqparse
import sqlite3
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="Username can not be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="Password can not be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": 'A user with username {} already exists.'.format(data['username'])}, 400

        connection = sqlite3.connect('data.sqlite')
        cursor = connection.cursor()
        query = 'INSERT INTO users VALUES (NULL, ?, ?);'
        cursor.execute(query, (data['username'], data['password'],))
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
