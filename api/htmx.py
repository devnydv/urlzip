from api import app
from flask import render_template

#just for test may be required letter
@app.route("/htmx")
def add_cat():
    return render_template("index.html")