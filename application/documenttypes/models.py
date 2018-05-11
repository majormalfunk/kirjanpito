from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint, text

class DocumentType(Descriptive):

    doctype = db.Column(db.String, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    ledgerdocuments = db.relationship("LedgerDocument", backref='documenttype_ledgerdocuments', lazy=True)

    __table_args__ = (UniqueConstraint('doctype', 'entity_id', name='documenttype_entity_uc'),)

    def __init__(self, doctype, name, description, inuse, entity_id):
        self.doctype = doctype
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id


