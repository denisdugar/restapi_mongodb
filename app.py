from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import request
import json

from numpy import string_

app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb+srv://<login>:<password>@cluster0.k6yf1.mongodb.net/<database>?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/count', methods=['GET'])
def count():
    return str(len(list(mongo.db.residents.find())))

@app.route('/rooms', methods=['GET'])
def home():
    if request.args.get('num'):
        if dumps(list(mongo.db.residents.find({'num': int(request.args.get('num'))}))):
            return  dumps(list(mongo.db.residents.find({'num': int(request.args.get('num'))})))
        else:
            return 'There is no room', 500
    if request.args.get('max'):
        if dumps(list(mongo.db.residents.find({'max_count_roommates' : int(request.args.get('max'))}))):
            return dumps(list(mongo.db.residents.find({'max_count_roommates' : int(request.args.get('max'))})))
        else:
            return 'There is no room', 500
    else:
        return dumps(list(mongo.db.residents.find()))

@app.route('/num=<num>/id', methods=['GET'])
def id(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return j["_id"]
    else:
        return 'There is no room', 500

@app.route('/num=<num>/roommates', methods=['GET'])
def roommates(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return dumps(list(j["roommates"]))
    else:
        return 'There is no room', 500

@app.route('/num=<num>/max_count_roommates', methods=['GET'])
def roommates_max(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return str(j["max_count_roommates"])
    else:
        return 'There is no room', 500

@app.route('/num=<num>/roommates_count', methods=['GET'])
def roommates_count(num):
    if json.loads(dumps(mongo.db.residents.find_one({'num': int(num)}))):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return str(len(j["roommates"]))
    else:
        return 'There is no room', 500  

@app.route('/num=<num>', methods=['PATCH'])
def change(num):
    if request.args.get('max'):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        if int(request.args.get('max'))>=len(j["roommates"]):
            mongo.db.residents.update_one({'num' : int(num)},{ "$set": { 'num': int(num) , 'max_count_roommates' : int(request.args.get('max')) }})
            return dumps(mongo.db.residents.find_one({'num': int(num)}))
        else:
            return 'Small max_roommates_count', 500
    if request.args.get('roommates'):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        if mongo.db.residents.find_one({'num': int(num)}) :
            if (j["max_count_roommates"] < len((request.args.get('roommates')).split())):
                return 'A lot of residents', 500
            else : 
                mongo.db.residents.update_one({'num' : int(num)},{ "$set": { 'num': int(num) , 'roommates' : (request.args.get('roommates')).split() }})
                return dumps(mongo.db.residents.find_one({'num': int(num)}))
        else :
            return 'This room does not exist'

@app.route('/create_room', methods=['POST'])
def add_room():
    if request.args.get('num'):
        if mongo.db.residents.find_one({'num' : int(request.args.get('num'))}):
            return 'This id alredy exist', 500
        else: 
            mongo.db.residents.insert_one({'num' : int(request.args.get('num')), "max_count_roommates" : int(request.args.get('max')), "roommates" : (request.args.get('roommates')).split()})
            return dumps(mongo.db.residents.find_one({'num': int(request.args.get('num'))}))
    else:
        mongo.db.residents.insert_one({'num' : int(len(list(mongo.db.residents.find())))+1, "max_count_roommates" : int(request.args.get('max')), "roommates" : (request.args.get('roommates')).split()})
        return dumps(mongo.db.residents.find_one({'num': int(len(list(mongo.db.residents.find())))}))

@app.route('/num=<num>', methods=['DELETE'])
def delete(num):
    if mongo.db.residents.find_one({'num': int(num)}) :
      mongo.db.residents.delete_one({'num': int(num)})
      return 'DELETED'
    else :
        return 'This num does not exist', 500