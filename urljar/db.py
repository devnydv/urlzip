import json
from pymongo.mongo_client import MongoClient
import os
import bcrypt
#database config
api = "mongodb+srv://bittumail:12356789@cluster0.fqrswkj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#api = os.getenv('db')

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
        if bcrypt.checkpw(password.encode("utf-16"), finduser[0]['password']):
            return {"massage":"You are logged in", "case":True}
        else:
            return {"massage":"Password do not match", "case":False}
        
# insert data to db when new user signpu
def saveuser(userdata):
    #print(userdata)
    collection.insert_one(userdata)

#edit users prifile
def editp(olduname, newuname, email, bio):
    filter = {"username": olduname}
    # Define the new values for the fields
    new_values = {"$set": {"username": newuname, "bio":bio, "email":email}}
    # Update the documents
    result = collection.update_many(filter, new_values)
    # Print the number of documents matched and modified
    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)


#check if username is unique  or not while signup
def userexist(uname):
    user = list(collection.find({"username": uname}))
    if user == []:
        return {"massage":"username is Unique", "case":True}
    else: 
        return {"massage":"username is already taken", "case":False}
    

# code for the user page
def usersdata(username):
    return list(collection.find({"username": username}))

# code to insert new category in db

def addcat(uname, cataval):
    #user = list(collection.find({"username": uname}))
    filter = {"username": uname}
    update = {"$push": {"category": cataval}}
    result = collection.update_one(filter, update)

#code to detele the category on x btn click
def delcat(uname, cataval):
    user = list(collection.find({"username": uname}))
    filter = {"username": uname}
    update = {"$pull": {"category": cataval}}
    result = collection.update_one(filter, update)

#find and return array to edit

def findarr(uname, ind):
    user = list(collection.find({"username": uname}))
    array = user[0]['links'][ind]
    return array

#save edited url details

def edited(uname, title, url, desc, ind):
    # Construct the update query to update the specific fields within the links array
    update_query = {
        f'links.{ind}.title': title,
        f'links.{ind}.url': url,
        f'links.{ind}.desc': desc
    }
    
    # Perform the update operation
    result = collection.update_one(
        {'username': uname, f'links.{ind}': {'$exists': True}},
        {'$set': update_query}
    )   
    
#delete a url card
def delcard(uname, id):
    collection.update_one(
    {"username": uname},
    {"$unset": {f"links.{id}":[id]}}
)
    collection.update_one(
    {"username": uname},
    {"$pull": {"links": None}}
)
    
# function to get all category to show in new url form
def getcat(uname):
    user = list(collection.find({"username": uname}))
    categories = user[0]["category"]
    return categories

# add new url to db
def addnew(uname, title, url, desc, cat ):
    new_object = {
        "title": title,
        "url": url,
        "desc": desc,
        "cat": cat

        }

# Query to find the document to update
    query = {"username": uname}

# Add the new object to the array
    collection.update_one(query, {"$push": {"links": new_object}})

# Fetch the updated document
    updated_document = collection.find_one(query)

# Get the array and find the index of the new object
    array = updated_document['links']
    new_object_index = array.index(new_object) if new_object in array else None
    return new_object_index