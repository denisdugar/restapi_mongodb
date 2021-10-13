from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import request
import json

from numpy import string_

app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb+srv://denis:254693178521@cluster0.k6yf1.mongodb.net/Hotel?retryWrites=true&w=majority"
mongo = PyMongo(app)

########## COUNT OF OBJECTS ############
@app.route('/count', methods=['GET'])
def count():
    return str(len(list(mongo.db.residents.find())))


########## SHOW ALL OBJECTS ############
@app.route('/rooms', methods=['GET']) 
def home():
    #################### SHOW OBJECT BY NUM ####################
    if request.args.get('num'): 
        if dumps(list(mongo.db.residents.find({'num': int(request.args.get('num'))}))):
            return  dumps(list(mongo.db.residents.find({'num': int(request.args.get('num'))})))
        else:
            return 'There is no room', 500
    ########## SHOW OBJECT BY MAX_COUNT_ROOMMATES ############
    if request.args.get('max'):
        if dumps(list(mongo.db.residents.find({'max_count_roommates' : int(request.args.get('max'))}))):
            return dumps(list(mongo.db.residents.find({'max_count_roommates' : int(request.args.get('max'))})))
        else:
            return 'There is no room', 500
    else:
        return dumps(list(mongo.db.residents.find()))


########## SHOW ID OBJECT BY NUM ############
@app.route('/num=<num>/id', methods=['GET'])
def id(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return j["_id"]
    else:
        return 'There is no room', 500


########## SHOW ARRAY OF ROOMMATES BY NUM ############
@app.route('/num=<num>/roommates', methods=['GET'])
def roommates(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return dumps(list(j["roommates"]))
    else:
        return 'There is no room', 500


########## SHOW MAX_COUNT_ROOMMATES BY NUM ############
@app.route('/num=<num>/max_count_roommates', methods=['GET'])
def roommates_max(num):
    if dumps(mongo.db.residents.find_one({'num': int(num)})):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return str(j["max_count_roommates"])
    else:
        return 'There is no room', 500


########## SHOW COUNT OF ROOMMATES BY NUM ############
@app.route('/num=<num>/roommates_count', methods=['GET'])
def roommates_count(num):
    if json.loads(dumps(mongo.db.residents.find_one({'num': int(num)}))):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        return str(len(j["roommates"]))
    else:
        return 'There is no room', 500  


########## UPDATE OBJECT BY NUM############
@app.route('/num=<num>', methods=['PATCH'])
def change(num):
    ########## UPDATE MAX_COUNT_ROOMMATES ############
    if request.args.get('max'):
        j = json.loads(dumps(mongo.db.residents.find_one({'num': int(num)})))
        if int(request.args.get('max'))>=len(j["roommates"]):
            mongo.db.residents.update_one({'num' : int(num)},{ "$set": { 'num': int(num) , 'max_count_roommates' : int(request.args.get('max')) }})
            return dumps(mongo.db.residents.find_one({'num': int(num)}))
        else:
            return 'Small max_roommates_count', 500
    ########## UPDATE ROOMMATES ############
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


########## CREATE OBJECT ############
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


########## DELETE OBJECT ############
@app.route('/num=<num>', methods=['DELETE'])
def delete(num):
    if mongo.db.residents.find_one({'num': int(num)}) :
      mongo.db.residents.delete_one({'num': int(num)})
      return 'DELETED'
    else :
        return 'This num does not exist', 500
