from application import db
from application.models import Base

class Entity(Base):

    code = db.Column(db.String(9), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    user_accounts = db.relationship("UserAccount", backref='entity_useraccounts', lazy=True)
    account_groups = db.relationship("AccountGroup", backref='entity_accountgroups', lazy=True)
    accounts = db.relationship("Account", backref='entity_accounts', lazy=True)
    domains = db.relationship("Domain", backref='entity_domains', lazy=True)
    activities = db.relationship("Activity", backref='entity_activities', lazy=True)

    def __init__(self, code, name, description):
        self.code = code
        self.name = name
        self.description = description
