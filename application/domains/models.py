from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint, text

class Domain(Descriptive):

    orderer = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable = False)

    ledgerrows = db.relationship("LedgerRow", backref='domain_ledgerrows', lazy=True)

    __table_args__ = (UniqueConstraint('code', 'entity_id', name='domain_entity_uc'),)

    def __init__(self, orderer, code, name, description, inuse, activity_id, entity_id):
        self.orderer = orderer
        self.code = code
        self.name = name
        self.description = description
        self.inuse = inuse
        self.activity_id = activity_id
        self.entity_id = entity_id

