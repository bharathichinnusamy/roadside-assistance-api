from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr



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
    children = relationship("Incident", backref="user")

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
class Service(db.Model):
     servicetype_id = db.Column(db.Integer, primary_key=True)
     servicetype_name = db.Column(db.String(80), unique=False, nullable=False)
     children = relationship("Incident", backref="service")

     def __repr__(self):
         return '<Service %r>' % self.servicetype_name

     def serialize(self):
         return {
             "servicetype_id": self.servicetype_id,
             "servicetype_name": self.servicetype_name
          }

class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Incident(TimestampMixin,db.Model):
    incident_id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, ForeignKey('hero.hero_id'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    latitude = db.Column(db.Float,unique=True, nullable=False)
    longitude = db.Column(db.Float,unique=True, nullable=False)
    servicetype_id = db.Column(db.Integer, db.ForeignKey("service.servicetype_id"))

    def __repr__(self):
        return '<Incident %r>' % self.Incident_id

    def serialize(self):
        return {
            "Incident_id": self.Incident_id,
            "hero_id": self.hero_id,
            "user_id": self.user_id,
            "servicetype_id": self.servicetype_id,
        }

