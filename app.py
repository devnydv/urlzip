from urljar import app
from htmx import htmx
from card import card

# test file is ignores by git need correction before push
app.register_blueprint(card)
app.register_blueprint(htmx)


if __name__=="__main__":
    app.run(debug=True)




