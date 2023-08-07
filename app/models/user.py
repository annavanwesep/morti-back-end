from app import db 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nulllable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
    
    @classmethod
    def from_dict(cls, user_details):
        new_user = cls(
            email=user_details["email"],
            first_name=user_details["first_name"],
            last_name=user_details["last_name"]
        )
        
        
        return new_user