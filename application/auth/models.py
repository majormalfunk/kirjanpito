from application import db
from application.models import Base
from sqlalchemy import UniqueConstraint

class UserAccount(Base):

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)
    role = db.Column(db.String(10))

    __table_args__ = (UniqueConstraint('username', name='account_username_uc'),)

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

    def get_role(self):
        return self.role

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def adminCount(entity_id):
        stmt = text("SELECT " +
            "COUNT(role) " +
            "FROM user_account " +
            "WHERE entity_id = :entity_id " +
            "AND role = 'admin' ").params(
                entity_id=entity_id)
        res = db.engine.execute(stmt)

        admins = 0
        for row in res:
            admins = row[0]
        return admins