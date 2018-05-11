from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint

class Account(Descriptive):

    number = db.Column(db.Integer, nullable=False)
    accountgroup_id = db.Column(db.Integer, db.ForeignKey("account_group.id"), nullable = False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    ledgerrows = db.relationship("LedgerRow", backref='account_ledgerrows', lazy=True)

    __table_args__ = (UniqueConstraint('number', 'entity_id', name='account_entity_uc'),)

    def __init__(self, number, name, description, inuse, accountgroup_id, entity_id):
        self.number = number
        self.name = name
        self.description = description
        self.inuse = inuse
        self.accountgroup_id = accountgroup_id
        self.entity_id = entity_id
    
