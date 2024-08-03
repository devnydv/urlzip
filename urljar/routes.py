from urljar import app
import bcrypt
from bleach import clean
from flask import render_template, flash, redirect, url_for, request, session
from urljar.forms import SignupForm, LoginForm
from urljar.db import userlogin, saveuser, userexist, usersdata, editp
#handle signup page 

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", 'POST'])
def signup():
    if request.method == "POST":
        form = SignupForm(request.form)
        if form.validate():
            # Handle form submission, e.g., save user data
            username = request.form['username'].lower()
            userval = userexist(username)
            if userval["case"]:
                bio = request.form["bio"]
                password = request.form['password']
                encodepass = bcrypt.hashpw(password.encode("utf-16"), bcrypt.gensalt())
                if bio =="":
                    bio = "Not available"
                formval = {"username": username,
                            "email": request.form['email'],
                            "bio": bio,
                            "password": encodepass,
                            "category":["seggestion"],
                            "links":[
                                {
                                    "title":"Link of your profile",
                                    "desc": "This is your profile link that you can share",
                                    "url": f'https://urljar.vercel.app/user/{username}',
                                    "cat":"seggestion"
                                },
                                {
                                    "title":"Second link for test",
                                    "desc": "This is your profile link that you can share",
                                    "url": f'https://urljar.vercel.app/user/{username}',
                                    "cat":"seggestion"
                                }
                            ]
                            }
                sendt = saveuser(formval)
                return redirect(url_for('login'))
                
            else:
                flash(userval["massage"])
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(request.form)
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        
        return render_template("signup.html", form=form)
    return render_template("signup.html")



@app.route("/login", methods=["GET", 'POST'])
def login():
    if "username" in session:
        uname = session["username"]
        return redirect(url_for('user', username=uname) )
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            # Handle form submission, e.g., save user data
            uname = request.form["username"].lower()
            logindata = userlogin(uname, request.form["password"])
            
            if logindata['case']:
                session["username"] = uname
                return redirect(url_for('user', username= uname))
            else:
                flash(logindata['massage'])
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        return render_template("login.html")
    return render_template("login.html")



# allow user to edit there profile
@app.route("/edit", methods=["GET", 'POST'])
def edit():
    if "username" in session:
        
        olduname = session["username"]
        #get olddata from db
        olddata = usersdata(olduname)
        oldemail = olddata[0]['email']
        oldbio = olddata[0]['bio']
        print(oldemail)
        if request.method == "POST":
            newuname = request.form["username"].lower()
            userval = userexist(newuname)
            
            if userval["case"]:
                session["username"]= newuname

            bio = clean(request.form["bio"])
            email = clean(request.form["email"])
            
            editp(olduname, newuname, email, bio)
                # update session name
                
            return redirect(url_for('user', username= newuname))
            #else:
                #return redirect(url_for('user', username= olduname))
        else:
            return render_template("editp.html", odata = {"oname":olduname, "oemail": oldemail, "obio":oldbio})
    else:
        return redirect(url_for('login'))

@app.route("/user/<username>")
def user(username):
    userval = userexist(username)
    if not userval["case"]:
        #print("username" in session)
        useralldata = usersdata(username)
        #print(useralldata)
        #useralldata = "lol"
        if "username" in session:

            sessionuname = session["username"]
            if sessionuname == username:
                return render_template("dashboard.html", username = sessionuname, userdata = useralldata) 
            else:  
                return render_template("profile.html",pname=username, username=sessionuname, userdata = useralldata, logged= True)
        else:
            return render_template("profile.html", pname=username, username=username, userdata = useralldata, logged= False)
    else:
        return render_template("nouser.html")
    

#api routes
# check if user already present or not 
@app.route("/username")
def user_exist():
    input = request.args.get("name").lower()
    userval = userexist(input)
    return userval

#logout user
@app.route("/logout")
def logout():
    if "username" in session:
        uname = session["username"]
        session.clear()
        return redirect(url_for('user', username= uname))
        #return "lol"
    else:
        #return redirect(url_for("login"))
        return redirect(url_for('user', username= uname))
        #return"lol"


@app.route("/terms")
def terms():
    if "username" in session:
        uname = session["username"]
        return render_template("terms.html", uname = uname)
    else :
        return render_template("terms.html", uname = "")

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error_404'))

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("nouser.html") , 404
    #return redirect(url_for('error_500'))

# Custom error pages
@app.route('/error_404')
def error_404():
    return render_template("nouser.html") , 404
    #return "This is a custom 404 error page.", 404

@app.route('/error_500')
def error_500():
    return render_template("nouser.html") , 404
    #return "This is a custom 500 error page.", 500
    