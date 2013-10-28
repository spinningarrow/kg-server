import os
import datetime
import time
import pymongo
from flask import Flask, Response, json, jsonify, request
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
@app.route(API_ROUTE_PREFIX + 'karung_gunis', methods=['GET', 'POST'])
def karung_gunis_array():
    if request.method == 'POST':
        user_id = karung_gunis.insert({
            'email': request.form['email'],
            'display_name': request.form['display_name'],
            'created': time.time()
        })

        result = karung_gunis.find_one({ '_id': ObjectId(user_id) })
        resp = Response(dumps(result), status=201, mimetype='application/json')

    else:
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
@app.route(API_ROUTE_PREFIX + 'sellers', methods=['GET', 'POST'])
def sellers_array():
    if request.method == 'POST':
        user_id = sellers.insert({
            'email': request.form['email'],
            'display_name': request.form['display_name'],
            'created': time.time()
        })

        result = sellers.find_one({ '_id': ObjectId(user_id) })
        resp = Response(dumps(result), status=201, mimetype='application/json')

    else:
        result = [document for document in sellers.find()]
        resp = Response(dumps(result), status=200, mimetype='application/json')

    return resp

# Get specific seller
@app.route(API_ROUTE_PREFIX + 'sellers/<_id>')
def seller_object(_id):
    result = sellers.find_one({ '_id': ObjectId(_id) })
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# List all advertisements or create a new advertisement
@app.route(API_ROUTE_PREFIX + 'advertisements', methods=['GET', 'POST'])
def advertisements_array():
    if request.method == 'POST':
        advertisement_id = advertisements.insert({
            'owner': request.form['owner'],
            'title': request.form['title'],
            'description': request.form['description'],
            'photo_url': request.form['photo_url'],
            'category': request.form['category'],
            'status': request.form['status'],
            'timing': request.form['timing'],
            'created': time.time()
        })

        result = advertisements.find_one({ '_id': ObjectId(advertisement_id) })
        resp = Response(dumps(result), status=201, mimetype='application/json')

    else:
        result = [document for document in advertisements.find()]
        resp = Response(dumps(result), status=200, mimetype='application/json')

    return resp

# Get open advertisements
@app.route(API_ROUTE_PREFIX + 'advertisements/open')
def advertisement_open():
    result = [document for document in advertisements.find({ 'status': 'OPEN' })]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Get advertisements by owner
@app.route(API_ROUTE_PREFIX + 'advertisements/owner/<_id>')
def advertisement_by_owner(_id):
    result = [document for document in advertisements.find({ 'owner': _id })]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Show advertisements newer than (or as new as) the provided timestamp
@app.route(API_ROUTE_PREFIX + 'advertisements/latest/<timestamp>')
def advertisement_latest(timestamp):
    result = [document for document in advertisements.find({ 'date_created': { '$gte': float(timestamp) } })]
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# Get specific advertisement
@app.route(API_ROUTE_PREFIX + 'advertisements/<_id>')
def advertisement_object(_id):
    result = advertisements.find_one({ '_id': ObjectId(_id) })
    resp = Response(dumps(result), status=200, mimetype='application/json')
    return resp

# List all users, or create a new one
@app.route(API_ROUTE_PREFIX + 'users', methods=['GET', 'POST'])
def users_array():
    if request.method == 'POST':
        # Check if a user by that email already exists
        if users.find_one({ 'email': request.form['email'] }):
            # Return 409 Conflicted
            resp = Response(dumps({ 'error': 'User already exists' }), status=409, mimetype='application/json')

        else:
            user_id = users.insert({
                'email': request.form['email'],
                'password': request.form['password'],
                'created': time.time()
            })

            result = users.find_one({ '_id': ObjectId(user_id) })
            # Return 201 Created
            resp = Response(dumps(result), status=201, mimetype='application/json')
    else:
        result = [document for document in users.find()]
        # Return 200 OK
        resp = Response(dumps(result), status=200, mimetype='application/json')

    return resp

# Get specific user by email address
@app.route(API_ROUTE_PREFIX + 'users/<email>')
def user_object(email):
    result = users.find_one({ 'email': email })

    # If no user found, reutrn a 404
    if result is None:
        resp = Response(dumps({ 'error': 'No user found' }), status=404, mimetype='application/json')

    # Otherwise check if the user is a KG or a seller and return the
    # role in the response
    else:
        role = None

        if karung_gunis.find_one({ 'email': result['email'] }):
            role = 'KARUNGGUNI'
        elif sellers.find_one({ 'email': result['email'] }):
            role = 'SELLER'

        result['role'] = role

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
