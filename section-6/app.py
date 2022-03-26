from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import identity, authenticate
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

JWT = JWT(app, authenticate, identity)  # /auth


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
