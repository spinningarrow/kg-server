import os
import datetime
import pymongo
from flask import Flask, Response, json, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

API_VERSION = '1.0'
API_ROUTE_PREFIX = '/api/' + API_VERSION + '/'
MONGO_URL = os.environ.get('MONGOHQ_URL')

app = Flask(__name__)
app.config['DEBUG'] = True

# Set up database
client = MongoClient(MONGO_URL)
db = client.app18404502
karung_gunis = db.karung_gunis
sellers = db.sellers
advertisements = db.advertisements
users = db.users

@app.route('/')
def index():
    return 'Nothing to do here.'

# List all karung gunis
@app.route(API_ROUTE_PREFIX + 'karung_gunis')
def karung_gunis_array():
    result = [document for document in karung_gunis.find()]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Get specific karung guni
@app.route(API_ROUTE_PREFIX + 'karung_gunis/<_id>')
def karung_guni_object(_id):
    result = karung_gunis.find_one({ '_id': ObjectId(_id) })
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# List all sellers
@app.route(API_ROUTE_PREFIX + 'sellers')
def sellers_array():
    result = [document for document in sellers.find()]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Get specific seller
@app.route(API_ROUTE_PREFIX + 'sellers/<_id>')
def seller_object(_id):
    result = sellers.find_one({ '_id': ObjectId(_id) })
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# List all advertisements
@app.route(API_ROUTE_PREFIX + 'advertisements')
def advertisements_array():
	result = [document for document in advertisements.find()]
	resp = Response(dumps(result), status=200, mimetype='application/json')
	return resp

# Get specific advertisement
@app.route(API_ROUTE_PREFIX + 'advertisements/<_id>')
def advertisement_object(_id):
	result = advertisements.find_one({ '_id': ObjectId(_id) })
	resp = Response(dumps(result), status=200, mimetype='application/json')
	return resp

# List all users
@app.route(API_ROUTE_PREFIX + 'users')
def users_array():
    result = [document for document in users.find()]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Get specific user by email address
@app.route(API_ROUTE_PREFIX + 'users/<email>')
def user_object(email):
    result = users.find_one({ 'email': email })
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Test method
@app.route('/mongo')
def mongo():
    # Specify the database
    # Print a list of collections
    # print db.collection_names()

    # Specify the collection, in this case 'monsters'

    # Get a count of the documents in this collection
    count = collection.count()
    # print "The number of documents you have in this collection is:", count

    # Create a document for a monster
    monster = {"name": "Vampirus",
               "occupation": "Blood Sucker",
               "tags": ["vampire", "teeth", "bat"],
               "date": datetime.datetime.utcnow()
    }

    # Insert the monster document into the monsters collection
    # monster_id = collection.insert(monster)

    # Print out our monster documents
    # for monster in collection.find():
    # print monster
    # results = collection.find()
    result = [dumps(document) for document in collection.find()]
    app.logger.debug(collection.find()[0])
    return jsonify(res=result)

# # Query for a particular monster
# print collection.find_one({"name": "Dracula"})

# Run Flask application
if __name__ == '__main__':
    app.run()
