from flask import render_template, flash, redirect, url_for, request, session
from htmx import htmx
from bleach import clean
from urljar.forms import catname
from urljar.db import addcat, delcat, findarr, edited, delcard, getcat, addnew



 # delete the category button 
@htmx.route("/catdelete", methods=["DELETE", "GET"])
def delete():
    #if request.method == "DELETE":
    if "username" in session:
        print("del")
        uname = session["username"]
        catval = clean(request.args.get('cat'))
        delcat(uname, catval)
        
        return "", 200
    else:
        return "Please login or sign up"   

  # html form to add category  
@htmx.route("/addcatdiv")
def addcatdiv():
    return '<div class="new-category-input"><form hx-post="/addcat" marhod="POST"  hx-swap="outerHTML" hx-target=".new-category-input"><input type="text" placeholder="Enter new category name" name="cat" ><button id="submitNewCategory">Add</button></form></div>'

@htmx.route("/addcat", methods=["GET", 'POST'])
def addcate():
    if "username" in session:
        uname = session["username"]
        if request.method == "POST":
            form = catname(request.form)
            print(list(form))
            if form.validate():
                catval =request.form["cat"]
                catval = catval.lower()
                capitalcat =catval.capitalize()
            #if catval == "":
                addcat(uname, catval)
                return f'<div><button class="category-btn" data-category="{capitalcat}" onclick="filter()">{capitalcat}<span class="delete-category" hx-get="/catdelete?cat={catval}" hx-target="closest div"hx-swap="outerHTMl">&times;</span></div><div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>'
            else:
                return '<div><button class="add-category-btn" hx-get="/addcatdiv" hx-target="closest div" hx-swap="outerHTML">Add Category</button></div>', 200
    else:
        return "Please log in"

# generate form to edit cards with previous values
@htmx.route("/cardedit", methods=["GET", 'POST'])
def cardedit():
    id = request.args.get('id')
    uname = session["username"]
    arrdata = findarr(uname, int(id))
    return render_template("cardedit.html", data= {"id": id, "arrdata": arrdata})

# save url edited data and return the edited data
@htmx.route("/saveedit", methods=["GET", 'POST'])
def saveedit():
    uname = session["username"]
    id = int(request.args.get('id'))
    title = clean(request.form["title"])
    url = clean(request.form["url"])
    desc = clean(request.form["desc"])
    
    edited(uname, title, url,desc, id)
    return f'''
      <h3 class="card-title">{title}</h3>
      <div class="url-link">
      <input type="text" class="link-input" value="{url}" readonly="">
        
        <button class="copy-btn">Copy</button>
      </div>
      <div class="categories">
              <span class="category-tag">category-tag</span>
          </div>
      <p class="description">{desc}</p>
      <div class="url-card-buttons">
        <button class="share-icon" title="Share this URL">&#128279;</button>
        <button hx-post="/cardedit?id={id}" hx-target="closest .url-card" hx-swap="innerHTML" class="edit-icon" title="Edit this URL">&#9998;</button>
        <button hx-post="/deleteurl?id={id}" hx-on::after-request="load()" class="delete-icon" title="Delete this URL">&#128465;</button>
      </div>
    '''
    
#delete url div
@htmx.route("/deleteurl", methods=["GET", 'POST'])
def deleteurl():
    uname = session["username"]
    id = request.args.get('id')
    delcard(uname, int(id))
    return ""

#return html form for adding url
@htmx.route("/addurlform", methods=["GET", 'POST'])
def addform():
    uname = session["username"]
    catd = getcat(uname)
    
    return render_template("urlform.html" , cat= catd)

# route to add new url details to db
@htmx.route("/addurl", methods=["GET", 'POST'])
def addurl():
    uname = session["username"]
    #id = 1 # get new from db
    title = clean(request.form["title"])
    url = clean(request.form["url"])
    desc = clean(request.form["desc"])
    cat = clean(request.form["options"].capitalize())
    id = addnew(uname, title, url, desc, cat )
    
    return f'''
    <div class="add-new-btn-container">
      <button class="add-new-btn" hx-post="/addurlform" hx-target="closest div" hx-swap="outerHTML">Add New URL</button>
    </div>
    <div class="url-card" data-category="{cat }">
      <h3 class="card-title">{title}</h3>
      <div class="url-link">
      <input type="text" class="link-input" value="{url}" readonly="">
        
        <button class="copy-btn">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        viewBox="0 0 16 16">
                        <path
                            d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z">
                        </path>
                        <path
                            d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z">
                        </path>
                    </svg>
        </button>
      </div>
      <p class="description">{desc}</p>
      <div class="url-card-buttons">
        <button class="share-icon" title="Share this URL">&#128279;</button>
        <button hx-post="/cardedit?id={id}" hx-target="closest .url-card" hx-swap="innerHTML" class="edit-icon" title="Edit this URL">&#9998;</button>
        <button hx-post="/deleteurl?id={id}" hx-on::after-request="load()" class="delete-icon" title="Delete this URL">&#128465;</button>
      </div>
    </div>
    

'''

@htmx.route("/del", methods=["GET", 'POST'])
def dele():
    return '''<div class="add-new-btn-container">
      <button class="add-new-btn" hx-post="/addurlform" hx-target="closest div" hx-swap="outerHTML">Add New URL</button>
    </div>'''
