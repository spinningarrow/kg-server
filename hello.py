import os
import datetime
import pymongo
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
# app.config['DEBUG'] = True

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/something')
def something():
	return 'something!'

@app.route('/mongo')
def mongo():
	# db = app18404502
	MONGO_URL = os.environ.get('MONGOHQ_URL')
	#connection = Connection(MONGO_URL)
	client = MongoClient(MONGO_URL)

	# Specify the database
	db = client.app18404502
	# Print a list of collections
	return jsonify(db.collection_names()[0])