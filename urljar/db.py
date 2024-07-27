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

#check if user exists or not while log in
def userlogin(uname, password):
    
    finduser = list(collection.find({"username": uname}))
    if finduser == []:
        return {"massage":"User name not fount", "case":False}
    else: 
        if password == finduser[0]['password']:
            return {"massage":"You are logged in", "case":True}
        else:
            return {"massage":"Password do not match", "case":False}
        
# insert data to db when new user signpu
def signup():
    collection.insert_one()


#check if username is unique  or not while signup
def userexist(uname):
    user = list(collection.find({"username": uname}))
    if user == []:
        return {"massage":"username is Unique", "case":True}
    else: 
        return {"massage":"username is already taken", "case":False}