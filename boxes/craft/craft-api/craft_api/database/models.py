# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from craft_api.database import db


class Brew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brewer = db.Column(db.String(80))
    name = db.Column(db.Text)
    style = db.Column(db.Text)
    abv = db.Column(db.Numeric)


    def __init__(self, brewer, name, style, abv):
        self.brewer = brewer
        self.name = name
        self.style = style
        self.abv = abv

    def __repr__(self):
        return '<Brew %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password