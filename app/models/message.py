from app import db 

class Message(db.Model):
    # __tablename__ = "messages" 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    text_message = db.Column(db.String(500))
    audio_message = db.Column(db.String)
    recipient_email = db.Column(db.String(345))
    recipient_id = db.Column(db.Integer)
    is_sent = db.Column(db.Boolean, default=False)
    
    #many messages can belong to one user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title,
            "text_message": self.text_message,
            "audio_message": self.audio_message,
            "recipient_email": self.recipient_email,
            "recipient_id": self.recipient_id,
            "is_sent": self.is_sent,
            "user_id": self.user_id
        }
    
    @classmethod
    def from_dict(cls, message_details):
        new_message = cls(
            title=message_details["title"],
            text_message=message_details["text_message"],
            audio_message=message_details["audio_message"],
            recipient_id=message_details["recipient_id"],
            is_sent=message_details["is_sent"],
            recipient_email=message_details["recipient_email"]
        )
        return new_message