from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False, default ="user")
    card_details = db.relationship("UserCardDetails", backref="bearer")

class UserCardDetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    attr_name = db.Column(db.String, nullable = False)
    attr_val = db.Column(db.String, nullable = False)
    cardname = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))