from application import db
from application.models import Descriptive
from sqlalchemy import UniqueConstraint, text

class Activity(Descriptive):

    orderer = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    domains = db.relationship("Domain", backref='activity_domains', lazy=True)

    __table_args__ = (UniqueConstraint('code', 'entity_id', name='activity_entity_uc'),)

    def __init__(self, orderer, code, name, description, inuse, entity_id):
        self.orderer = orderer
        self.code = code
        self.name = name
        self.description = description
        self.inuse = inuse
        self.entity_id = entity_id

    @staticmethod
    def findAllActivitiesAndDomains(entity_id):
        stmt = text("SELECT " +
            "ac.id, ac.orderer, ac.code, ac.name, ac.description, ac.inuse, " +
            "dm.id, dm.orderer, dm.code, dm.name, dm.description, dm.inuse " +
            "FROM activity ac " +
            "LEFT JOIN domain dm on ac.id = dm.activity_id " +
            "WHERE ac.entity_id = :entity_id " +
            "ORDER BY ac.orderer, dm.orderer").params(entity_id=entity_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"activity_id":row[0],
                            "activity_orderer":row[1],
                            "activity_code":row[2],
                            "activity_name":row[3],
                            "activity_description":row[4],
                            "activity_inuse":row[5],
                            "domain_id":row[6],
                            "domain_orderer":row[7],
                            "domain_code":row[8],
                            "domain_name":row[9],
                            "domain_description":row[10],
                            "domain_inuse":row[11]})
        return response
