from flask import render_template, flash, redirect, url_for, request, session
from urljar import app
from urljar.db import addcat, delcat
# delete the category button 
# this is demo only and data from db is not deleted
@app.route("/catdelete", methods=["DELETE", "GET"])
def delete():
    #if request.method == "DELETE":
    if "username" in session:
        uname = session["username"]
        catval = request.args.get('cat')
        delcat(uname, catval)
        return "", 200
    else:
        return "Please login or sign up"
    
@app.route("/addcatdiv")
def addcatdiv():
    return '<div class="new-category-input"><form hx-post="/addcat" marhod="POST"  hx-swap="outerHTML" hx-target=".new-category-input"><input type="text" placeholder="Enter new category name" name="cat"><button id="submitNewCategory">Add</button></form></div>'

@app.route("/addcat", methods=["GET", 'POST'])
def addcate():
    if "username" in session:
        uname = session["username"]
        if request.method == "POST":
            catval =request.form["cat"]
            catval = catval.lower()
        
            if catval == "":
                return '<div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>', 200
            else:
                addcat(uname, catval)
                return f'<div><button class="category-btn" data-category="{catval}" onclick="filter()">{catval}<span class="delete-category" hx-delete="/catdelete" hx-target="closest div"hx-swap="outerHTMl">&times;</span></div><div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>'
    else:
        return "Please log in"

    