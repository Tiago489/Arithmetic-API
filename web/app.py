from flask import Flask, jsonify, request

#import API support from flask_restful.
from flask_restful import Api, Resource

#import Python's os module for operating system support.
import os

# import MongoClient from pymongo for MongoDB support.
from pymongo import MongoClient

#define app
app = Flask(__name__)
#define Api
api = Api(app)
#define client and database
client = MongoClient("mongodb://db:27017") #27017 is the default port for mongodb
db = client.myNewDB
VisitCounter = db["VisitCounter"]
VisitCounter.insert({
    'num_of_visits': 0
})
#defiine class Visit
class Visit(Resource):
    def get(self):
        prev_count = VisitCounter.find({})[0]['num_of_visits']
        new_count = prev_count + 1
        VisitCounter.update({}, {"$set":{"num_of_visits":new_count}})
        return str("Hello user, just fyi, this API service has been used " + str(new_count) + " times.")
#define a check for the posted data
def checkPostedData(postedData, functionName):
    if functionName == "add" or functionName == "subtract" or functionName == "multiply":
        if "x" not in postedData or "y" not in postedData:
            return str("You need to send 2 numbers my way if you want me to calculate them.")
        else:
            return 200
    elif functionName == "divide":
        if "x" not in postedData or "y" not in postedData:
            return str("You need to send 2 numbers my way if you want me to calculate them.")
        elif int(postedData["x"]) == 0:
            return str("x cannot be zero (neither can y by the matter), but you can choose pretty much any other number.")
        elif int(postedData["y"]) == 0:
            return str("y cannot be zero (neither can x by the matter), but you can choose pretty much any other number.")
        else:
            return 200

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")

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

        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code' : 200
        }
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

#add resources
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Divide, "/divide")
api.add_resource(Multiply, "/multiply")
api.add_resource(Visit, "/")
#define root route
@app.route('/')
def hello_world():
    return "Hello World"

if __name__=="__main__":
    app.run(host='0.0.0.0')
