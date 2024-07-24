import json
from pymongo.mongo_client import MongoClient
import os

#database config
api = "mongodb+srv://bittumail:12356789@cluster0.fqrswkj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#api = os.getenv('mongo")

url = api
client = MongoClient(url)
db = client.urljar
collection = db.users

def userlogin(uname, password):
    
    finduser = list(collection.find({"username": uname}))
    if finduser == []:
        return {"massage":"User name not fount", "case":False}
    else: 
        if password == finduser[0]['password']:
            return {"massage":"You are logged in", "case":True}
        else:
            return {"massage":"Password do not match", "case":False}

def signup():
    collection.insert_one()