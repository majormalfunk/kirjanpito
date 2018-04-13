from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint

class AccountGroup(Descriptive):

    number = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    accounts = db.relationship("Account", backref='accountgroup_accounts', lazy=True)

    __table_args__ = (UniqueConstraint('number', 'entity_id', name='accountgroup_entity_uc'),)

    def __init__(self, number, name, description, inuse, entity_id):
        self.number = number
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id
