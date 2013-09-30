import os
import datetime
import pymongo
from flask import Flask, json, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

API_VERSION = '1.0'
API_ROUTE_PREFIX = '/api/' + API_VERSION + '/'
MONGO_URL = os.environ.get('MONGOHQ_URL')

app = Flask(__name__)
app.config['DEBUG'] = True

# Set up database
client = MongoClient(MONGO_URL)
db = client.app18404502
collection = db.kgdata

@app.route('/')
def index():
	return 'Nothing to do here.'

# List all karung gunis
@app.route(API_ROUTE_PREFIX + 'karunggunis')
def karungGunis():
	result = [dumps(document) for document in collection.find({ 'role': 'kg' })]
	return jsonify(result=result)

# List all sellers
@app.route(API_ROUTE_PREFIX + 'sellers')
def sellers():
	result = [dumps(document) for document in collection.find({ 'role': 'seller' })]
	return jsonify(result=result)

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