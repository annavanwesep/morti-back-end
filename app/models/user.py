from app import db

# Association table
trust_link = db.Table(
    'trust_links',
    db.Column('current_user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('trusted_user_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    #one user can create many messages, refactor to use backref
    messages = db.relationship("Message", backref="user", lazy=True)

    #many to many relationship, many users can trust many users
    trusted_users = db.relationship("User", 
        secondary=trust_link, 
        primaryjoin=(trust_link.c.current_user_id == id),
        secondaryjoin=(trust_link.c.trusted_user_id == id),
        backref=db.backref('trust_links', lazy='dynamic'), 
        lazy='dynamic')
    
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