from flask import Flask

app = Flask(__name__)
app.secret_key ="doNotTryToSuck"

from urljar import routes

#from htmx import route


