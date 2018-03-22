from application import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    inuse = db.Column(db.Boolean, nullable=False)

    def __init__(self, code, name, inuse):
        self.code = code
        self.name = name
        self.inuse = inuse
