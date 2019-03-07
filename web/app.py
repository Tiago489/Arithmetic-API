#imports the Flask framework, jsonify service formats the data passed inside to JSON format (as used in the return statements) and request service helps te application to keep track of the request object
from flask import Flask, jsonify, request

#import services from flask_restful, an extension of flask that provides support for building APIs
#Api service is the main entry point for the application, needs to be initialized with the flask application
#Resource assists with the creation of custom method classes, using Resource as the method's argument
from flask_restful import Api, Resource

#import Python's os module for a way to use operating system functionality.
import os

# PyMongo contains tools to and is the recommended way to work with MongoDB in Python
# MongoClient provides more tools to interacting with MongoDB
from pymongo import MongoClient

# define and initialize the flask application
app = Flask(__name__)
# initializes flask_restful's Api service in the application
api = Api(app)
# initializes mongodb and runs it on its default port 27017
client = MongoClient("mongodb://db:27017")
# creates and initializes the database to be used by the application
db = client.myNewDB
# creates the collection to be used by the application
VisitCounter = db["VisitCounter"]
# inserts document in the collection
VisitCounter.insert({
    'num_of_visits': 0
})

#this class keeps tracks of the number of times our api has been requested
class Visit(Resource):
    # defines what happens when a GET request is submitted by the user
    def get(self):
        #looks at the current number of visits
        prev_count = VisitCounter.find({})[0]['num_of_visits']
        #adds one to the number each time the service is called
        new_count = prev_count + 1
        #updates the database with the new number of visits
        VisitCounter.update({}, {"$set":{"num_of_visits":new_count}})
        #displays to the user how many times our service has been visited
        return str("Hello user, just fyi, this API service has been used " + str(new_count) + " times.")
# function that checks if user is sending in 2 values to be calculated as well as check to see if the user is trying to divide by zero
def checkPostedData(postedData, functionName):
    if functionName == "add" or functionName == "subtract" or functionName == "multiply":
        #if either x or y are not present in the postedData, throws error to user
        if "x" not in postedData or "y" not in postedData:
            return str("You need to send 2 numbers my way if you want me to calculate them.")
        else:
            return 200
    #throws error if user tries to divide by zero
    elif functionName == "divide":
        if "x" not in postedData or "y" not in postedData:
            return str("You need to send 2 numbers my way if you want me to calculate them.")
        elif int(postedData["x"]) == 0:
            return str("x cannot be zero (neither can y by the matter), but you can choose pretty much any other number.")
        elif int(postedData["y"]) == 0:
            return str("y cannot be zero (neither can x by the matter), but you can choose pretty much any other number.")
        else:
            return 200

#define the Add class
class Add(Resource):
    #define how the app is to behave when a POST request calls this service
    def post(self):
        #.get_json parses and returns the data as json
        postedData = request.get_json()
        #calls the checkPostedData within the context of the add method
        status_code = checkPostedData(postedData, "add")

        #handles error messages
        if status_code != 200:
            retJson = {
                'Message': "There was an error",
                'Status Code': status_code
            }
            return jsonify(retJson)

        #asigns the values of x and y entered by the user to local x and y variables
        x = postedData["x"]
        y = postedData["y"]

        #ensures x and y are integers
        x = int(x)
        y = int(y)

        #handles the actual arithmetic operation
        ret = x + y
        #prepares the json response
        retMap = {
            'Message': ret,
            'Status Code' : 200
        }
        #returns jsonified version of the response
        return jsonify(retMap)

#define class Subtract
class Subtract(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "subtract")

        if status_code != 200:
            retJson = {
                'Message': "There was an error",
                'Status Code': status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x - y
        retMap = {
            'Message': ret,
            'Status Code' : 200
        }
        return jsonify(retMap)
#define class Divide
class Divide(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "divide")

        if status_code != 200:
            retJson = {
                'Message': "There was an error",
                'Status Code': status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x / y
        retMap = {
            'Message': ret,
            'Status Code' : 200
        }
        return jsonify(retMap)
#define class Multiply
class Multiply(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "multiply")

        if status_code != 200:
            retJson = {
                'Message': "There was an error",
                'Status Code': status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]

        x = int(x)
        y = int(y)

        ret = x * y
        retMap = {
            'Message': ret,
            'Status Code' : 200
        }
        return jsonify(retMap)

#add resources to the api, that the user can call on by going to the url listed in the parantheses
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Divide, "/divide")
api.add_resource(Multiply, "/multiply")
api.add_resource(Visit, "/")

#define root route
@app.route('/')
def hello_world():
    return "Hello World"

#initiates the application and runs it in the given port for Docker
if __name__=="__main__":
    app.run(host='0.0.0.0')
