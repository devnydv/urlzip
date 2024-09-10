from flask import Blueprint

htmx = Blueprint("htmx", __name__, template_folder='templates')

from htmx import route