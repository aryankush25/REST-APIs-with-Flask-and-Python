from crypt import methods
from flask import Flask
app = Flask('app')


@app.route('/store', methods=['POST'])
def create_store():
    pass


@app.route('/store<string:name>')
def get_store(name):
    pass


@app.route('/store')
def get_stores():
    pass


@app.route('/store<string:name>/items', methods=['POST'])
def create_store_items(name):
    pass


@app.route('/store<string:name>/items')
def get_store_items(name):
    pass


app.run(port=8080)
