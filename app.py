from flask import Flask , render_template, flash, redirect, url_for, request
from forms import SignupForm, LoginForm
from db import userlogin

app = Flask(__name__)
app.secret_key ="doNotTryToSuck"
@app.route("/")
def home():
    return render_template("index.html")



#handle signup page 
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
                return redirect(url_for('user'))
            else:
                flash(logindata['massage'], 'success')
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        return render_template("login.html")
    return render_template("login.html")

@app.route("/edit")
def edit():
    return render_template("editp.html")

@app.route("/user")
def user():
    return render_template("user.html")

if __name__=="__main__":
    app.run(debug=True)


