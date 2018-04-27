from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint, text

class Activity(Descriptive):

    code = db.Column(db.Integer, nullable=False)
    orderer = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    __table_args__ = (UniqueConstraint('code', 'entity_id', name='activity_entity_uc'),)

    def __init__(self, orderer, code, name, description, inuse, entity_id):
        self.orderer = orderer
        self.code = code
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id

