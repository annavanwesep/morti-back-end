from app import db 

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(500))
    recipient_email = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            "message_id": self.id, 
            "message": self.message,
            "recipient_email": self.recipient_email
        }
    
    @classmethod
    def from_dict(cls, message_details):
        new_message = cls(
            message=message_details["message"],
            recipient_email=message_details["recipient_email"]
        )
        return new_message