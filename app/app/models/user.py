from app import db 

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    # password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
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