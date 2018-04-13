from application import db
from sqlalchemy import UniqueConstraint

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    inuse = db.Column(db.Boolean, nullable=False)

    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable = False)

    __table_args__ = (UniqueConstraint('number', 'entity_id', name='account_entity_code_uc'),)

    def __init__(self, number, name, description, inuse, entity_id):
        self.number = number
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id
