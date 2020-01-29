from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    share_phone = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "share_phone": self.share_phone
        }
class Hero(db.Model):
    hero_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    zip_code = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    share_phone = db.Column(db.Integer, nullable=False)
    children = relationship("Incident", backref="hero")
    #children = relationship("Incident")

    def __repr__(self):
        return '<Hero %r>' % self.first_name

    def serialize(self):
        return {
            "hero_id": self.hero_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "zip_code": self.zip_code,
            "phone": self.phone,
            "share_phone": self.share_phone
        }

# class Service(db.Model):
#     servicetype_id = db.Column(db.Integer, primary_key=True)
#     servicetype_name = db.Column(db.String(80), unique=False, nullable=False)
#     children = relationship("Incident")

#     def __repr__(self):
#         return '<Service %r>' % self.servicetype_name

#     def serialize(self):
#         return {
#             "service_id": self.user_id,
#             "servicetype_name": self.servicetype_name
#         }
class Incident(db.Model):
    Incident_id = db.Column(db.Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('hero.hero_id'))
   # hero_id = db.Column(db.Integer, db.ForeignKey("Hero.hero_id"))
    #user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))
   # servicetype_id = db.Column(db.Integer, db.ForeignKey("Service.servicetype_id"))
    #timestamp = 

    def __repr__(self):
        return '<Service %r>' % self.servicetype_name

    def serialize(self):
        return {
            #"service_id": self.user_id,
            #"servicetype_name": self.servicetype_name
        }