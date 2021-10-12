from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
import json

from numpy import string_

app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb+srv://<login>:<password>@cluster0.k6yf1.mongodb.net/<database>?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def home():
    return dumps(list(mongo.db.residents.find()))

@app.route('/num=<num>', methods=['GET'])
def room(num):
    return  dumps(mongo.db.residents.find_one({'num': int(num)}))

@app.route('/num=<num>/id', methods=['GET'])
def id(num):
    j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
    return j["_id"]

@app.route('/num=<num>/max_roommates', methods=['GET'])
def max_roommates_count(num):
    j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
    return str(j["max_count_roommates"])

@app.route('/num=<num>/roommates', methods=['GET'])
def roommates(num):
    j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
    return dumps(list(j["roommates"]))

@app.route('/num=<num>/roommates_count', methods=['GET'])
def roommates_count(num):
    j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
    return str(len(j["roommates"]))

@app.route('/max_count_roommates=<max>', methods=['GET'])
def all_max(max):
    return dumps(list(mongo.db.residents.find({'max_count_roommates' : int(max)})))

@app.route('/num=<num>|max_count_roommates=<max_num>', methods=['PATCH'])
def change_max(num, max_num):
    mongo.db.residents.update_one({'num' : int(num)},{ "$set": { 'num': int(num) , 'max_count_roommates' : int(max_num) }})
    return dumps(mongo.db.residents.find_one({'num': int(num)}))

@app.route('/num=<num>|roommates=<room>', methods=['PATCH'])
def change_roommates(num, room):
    j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
    if mongo.db.residents.find_one({'num': int(num)}) :
        if (j["max_count_roommates"] < len(room.split())):
            return 'A lot of residents'
        else : 
            mongo.db.residents.update_one({'num' : int(num)},{ "$set": { 'num': int(num) , 'roommates' : room.split() }})
            return dumps(mongo.db.residents.find_one({'num': int(num)}))
    else :
        return 'This room does not exist'

@app.route('/num=<num>|max_count_roommates=<max>|roommmates=<room>', methods=['POST'])
def add_room(num, max, room):
    if mongo.db.residents.find_one({'num' : int(num)}):
        return 'This id alredy exist'
    else: 
        x = mongo.db.residents.insert_one({'num' : int(num), "max_count_roommates" : int(max), "roommates" : room.split()})
        return dumps(mongo.db.residents.find_one({'num': int(num)}))

@app.route('/num=<num>', methods=['DELETE'])
def delete(num):
    if mongo.db.residents.find_one({'num': int(num)}) :
      mongo.db.residents.delete_one({'num': int(num)})
      return 'DELETED'
    else :
        return 'This num does not exist'