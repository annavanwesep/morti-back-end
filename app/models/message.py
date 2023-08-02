from app import db 

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    text_message = db.Column(db.String(500))
    audio_message = db.Column(db.String(500))
    id_recipient = db.Column(db.Integer)
    # is_sent = db.Column(db.BooleanProperty)
    recipient_email = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship("User", back_populates="messages")
    
    def to_dict(self):
        return {
            "id": self.id, 
            "title": self.title,
            "text_message": self.text_message,
            "audio_message": self.audio_message,
            "id_recipient": self.id_recipient,
            "is_sent": self.is_sent,
            "recipient_email": self.recipient_email
        }
    
    @classmethod
    def from_dict(cls, message_details):
        new_message = cls(
            title=message_details["title"],
            text_message=message_details["text_message"],
            audio_message=message_details["audio_message"],
            id_recipient=message_details["id_recipient"],
            is_sent=message_details["is_sent"],
            recipient_email=message_details["recipient_email"]
        )
        return new_message