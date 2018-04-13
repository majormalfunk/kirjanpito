from application import db

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

class Descriptive(Base):

    __abstract__ = True

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    inuse = db.Column(db.Boolean, nullable=False)

