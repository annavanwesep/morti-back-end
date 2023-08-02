from app import db 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    messages = db.relationship("Message", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
    
    @classmethod
    def from_dict(cls, user_details):
        return cls(
            email=user_details["email"],
            first_name=user_details["first_name"],
            last_name=user_details["last_name"]
        )
