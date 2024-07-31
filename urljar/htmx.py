from flask import render_template, flash, redirect, url_for, request, session
from urljar import app
from urljar.db import addcat, delcat, findarr, edited, delcard, getcat, addnew


# delete the category button 
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
    

  # html form to add category  
@app.route("/addcatdiv")
def addcatdiv():
    return '<div class="new-category-input"><form hx-post="/addcat" marhod="POST"  hx-swap="outerHTML" hx-target=".new-category-input"><input type="text" placeholder="Enter new category name" name="cat" ><button id="submitNewCategory">Add</button></form></div>'

@app.route("/addcat", methods=["GET", 'POST'])
def addcate():
    if "username" in session:
        uname = session["username"]
        if request.method == "POST":
            catval =request.form["cat"]
            catval = catval.lower()
            capitalcat =catval.capitalize()
            if catval == "":
                return '<div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>', 200
            else:
                addcat(uname, catval)
                return f'<div><button class="category-btn" data-category="{capitalcat}" onclick="filter()">{capitalcat}<span class="delete-category" hx-delete="/catdelete" hx-target="closest div"hx-swap="outerHTMl">&times;</span></div><div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>'
    else:
        return "Please log in"

# generate form to edit cards with previous values
@app.route("/cardedit", methods=["GET", 'POST'])
def cardedit():
    id = request.args.get('id')
    uname = session["username"]
    arrdata = findarr(uname, int(id))
    
    return f'''<form hx-post="/saveedit?id={id}" hx-swap="innerHTML" hx-target="closest .url-card">
        <div class="new-card-input">
          <input type="text" id="title" name="title" placeholder="Title for the URL" value="{arrdata['title']}" required>
          <input type="url" name="url" placeholder=" Edit Url" value="{arrdata['url']}" required>
          <input type="text" name="desc" placeholder="Edit description" value="{arrdata['desc']}" required>
        </div>
        <button class="add-new-btn"> Confirm Edit</button>
        
      </form>'''

@app.route("/saveedit", methods=["GET", 'POST'])
def saveedit():
    uname = session["username"]
    id = request.args.get('id')
    title = request.form["title"]
    url = request.form["url"]
    desc = request.form["desc"]
    
    edited(uname, title, url,desc, id)
    return f'''
      <h3>{title}</h3>
      <div class="url-link">
        <a href="{url}" target="_blank">{url}</a>
        <button class="copy-btn">Copy</button>
      </div>
      <p>{desc}</p>
      <div class="url-card-buttons">
        <button class="share-icon" title="Share this URL">&#128279;</button>
        <button hx-post="/cardedit?id={id}" hx-target="closest .url-card" hx-swap="innerHTML" class="edit-icon" title="Edit this URL">&#9998;</button>
        <button hx-post="/deleteurl?id={id}" hx-on::after-request="load()" class="delete-icon" title="Delete this URL">&#128465;</button>
      </div>
    '''
    
#delete url div
@app.route("/deleteurl", methods=["GET", 'POST'])
def deleteurl():
    uname = session["username"]
    id = request.args.get('id')
    delcard(uname, int(id))
    return ""

#return html form for adding url
@app.route("/addurlform", methods=["GET", 'POST'])
def addform():
    uname = session["username"]
    catd = getcat(uname)
    
    return render_template("urlform.html" , cat= catd)

# route to add new url details to db
@app.route("/addurl", methods=["GET", 'POST'])
def addurl():
    uname = session["username"]
    id = 1 # get new from db
    title = request.form["title"]
    url = request.form["url"]
    desc = request.form["desc"]
    cat = request.form["options"].capitalize()
    id = addnew(uname, title, url, desc, cat )
    
    return f'''
    <div class="url-card" data-category="{cat }">
      <h3>{title}</h3>
      <div class="url-link">
        <a href="{url}">{url}</a>
        <button class="copy-btn">Copy</button>
      </div>
      <p>{desc}</p>
      <div class="url-card-buttons">
        <button class="share-icon" title="Share this URL">&#128279;</button>
        <button hx-post="/cardedit?id={id}" hx-target="closest .url-card" hx-swap="innerHTML" class="edit-icon" title="Edit this URL">&#9998;</button>
        <button hx-post="/deleteurl?id={id}" hx-on::after-request="load()" class="delete-icon" title="Delete this URL">&#128465;</button>
      </div>
    </div>
    <div class="add-new-btn-container">
      <button class="add-new-btn" hx-post="/addurlform" hx-target="closest div" hx-swap="outerHTML">Add New URL</button>
    </div>

'''

@app.route("/del", methods=["GET", 'POST'])
def dele():
    return '''<div class="add-new-btn-container">
      <button class="add-new-btn" hx-post="/addurlform" hx-target="closest div" hx-swap="outerHTML">Add New URL</button>
    </div>'''
