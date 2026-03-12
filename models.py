from flask_sqlalchemy import *

db= SQLAlchemy()

class Favorite (db.Model):
    id = db.Column (db.Integer,  primary_key = True)
    api_id = db.Column (db.Integer, unique = True)
    name = db.Column (db.String(100) )
    imagen = db.Column (db.String(255))


