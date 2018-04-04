from application import db

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    code = db.Column(db.String(9), nullable=True, unique=True)
    name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    user_accounts = db.relationship("UserAccount", backref='user_account', lazy=True)
    accounts = db.relationship("Account", backref='account', lazy=True)

    def __init__(self, code, name, description):
        self.code = code
        self.name = name
        self.description = description
