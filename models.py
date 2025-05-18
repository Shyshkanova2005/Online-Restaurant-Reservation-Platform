from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON 

db = SQLAlchemy()

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    table = db.Column(db.String(10), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    during = db.Column(db.String(10), nullable=False)  
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)  
    email = db.Column(db.String(100), nullable=False)
    order = db.Column(JSON)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    