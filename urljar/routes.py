from urljar import app
from flask import render_template, flash, redirect, url_for, request, session
from urljar.forms import SignupForm, LoginForm
from urljar.db import userlogin, signup, userexist
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
            print(request.form['username'])
            
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(request.form)
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        
        return render_template("signup.html", form=form)
    return render_template("signup.html")



@app.route("/login", methods=["GET", 'POST'])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            # Handle form submission, e.g., save user data
            logindata = userlogin(request.form["username"], request.form["password"])
            
            if logindata['case']:
                session["username"] = request.form["username"]
                return redirect(url_for('user', username= request.form["username"]))
            else:
                flash(logindata['massage'])
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        return render_template("login.html")
    return render_template("login.html")

@app.route("/edit")
def edit():
    return render_template("editp.html")

@app.route("/<username>")
def user(username):
    sessionuname = session["username"]
    if username == sessionuname:
        return render_template("dashboard.html", username = sessionuname)
    else:
        return render_template("profile.html", username=username )

#api routes
@app.route("/username")
def user_exist():
    #pass username that will be sent through get request
    #checkuser = userexist()
    return render_template("user.html")