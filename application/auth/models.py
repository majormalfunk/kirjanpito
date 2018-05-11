from application import db
from application.models import Base

class UserAccount(Base):

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)
    role = db.Column(db.String(10))

    def __init__(self, name, username, password, entity_id, role) :
        self.name = name
        self.username = username
        self.password = password
        self.entity_id = entity_id
        self.role = role
  
    def get_id(self):
        return self.id

    def get_entity_id(self):
        return self.entity_id

    def get_username(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
