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

class Lockable(Base):

    __abstract__ = True

    closed = db.Column(db.Boolean, nullable=False)
    locked = db.Column(db.Boolean, nullable=False)

class TimeBased(Lockable):

    __abstract__ = True

    startdate = db.Column(db.Date, nullable=False)
    enddate = db.Column(db.Date, nullable=False)