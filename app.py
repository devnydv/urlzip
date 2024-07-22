from flask import Flask , render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/edit")
def edit():
    return render_template("editp.html")

if __name__=="__main__":
    app.run(debug=True)


