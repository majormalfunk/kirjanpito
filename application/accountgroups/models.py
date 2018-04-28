from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint, text

class AccountGroup(Descriptive):

    number = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    accounts = db.relationship("Account", backref='accountgroup_accounts', lazy=True)

    __table_args__ = (UniqueConstraint('number', 'entity_id', name='accountgroup_entity_uc'),)

    def __init__(self, number, name, description, inuse, entity_id):
        self.number = number
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id

    @staticmethod
    def findAllGroupsAndAccounts(entity_id):
        stmt = text("SELECT " +
            "ag.id, ag.number, ag.name, ag.description, ag.inuse, " +
            "a.id, a.number, a.name, a.description, a.inuse " +
            "FROM account_group ag " +
            "LEFT JOIN account a on ag.id = a.accountgroup_id " +
            "WHERE ag.entity_id = :entity_id " +
            "ORDER BY ag.number, a.number").params(entity_id=entity_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"account_group_id":row[0],
                            "account_group_number":row[1],
                            "account_group_name":row[2],
                            "account_group_description":row[3],
                            "account_group_inuse":row[4],
                            "account_id":row[5],
                            "account_number":row[6],
                            "account_name":row[7],
                            "account_description":row[8],
                            "account_inuse":row[9]})
        return response
