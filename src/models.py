from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    is_hero = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    zip_code = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(80), unique=True, nullable=False)
    share_phone = db.Column(db.Boolean, server_default=expression.true(), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "is_hero": self.is_hero,
            "zip_code": self.zip_code,
            "phone": self.phone,
            "share_phone": self.share_phone
        }

class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    servicetype_name = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<Service %r>' % self.servicetype_name

    def serialize(self):
        return {
            "service_id": self.user_id,
            "servicetype_name": self.servicetype_name
        }