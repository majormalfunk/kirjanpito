from application import db
from application.models import Base
from sqlalchemy import UniqueConstraint, text

class LedgerDocument(Base):

    documenttype_id = db.Column(db.Integer, db.ForeignKey("document_type.id"), nullable = False)
    documentnumber = db.Column(db.Integer, nullable=False)
    ledgerdate = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    recorded_by = db.Column(db.String(144), nullable = False)
    approved_by = db.Column(db.String(144), nullable = True)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    ledgerrows = db.relationship("LedgerRow", backref='ledgerdocument_ledgerrows', lazy=True)

    __table_args__ = (UniqueConstraint('documentnumber', 'documenttype_id', 'entity_id', name='ledgerdoc_number_type_entity_uc'),)

    def __init__(self, documenttype_id, documentnumber, ledgerdate,
                    description, recorded_by, approved_by, entity_id):
        self.documenttype_id = documenttype_id
        self.documentnumber = documentnumber
        self.ledgerdate = ledgerdate
        self.description = description
        self.recorded_by = recorded_by
        self.approved_by = approved_by
        self.entity_id = entity_id

    @staticmethod
    def findLedgerDocuments(entity_id, fiscalyear_id, fiscalperiod_id):
        stmt = text("SELECT " +
            "ld.id, ld.documenttype_id, dt.doctype, ld.documentnumber, " +
            "ld.ledgerdate, fy.name, fp.name, " +
            "ld.description, ld.recorded_by, ld.approved_by, ld.entity_id " +
            "FROM ledger_document ld, document_type dt, fiscal_year fy, fiscal_period fp " +
            "WHERE dt.id = ld.documenttype_id " +
            "AND ld.ledgerdate >= fp.startdate AND ld.ledgerdate <= fp.enddate " +
            "AND fy.id = fp.fiscalyear_id " +  
            "AND ld.entity_id = :entity_id " +
            "AND dt.entity_id = ld.entity_id " +
            "AND fy.entity_id = ld.entity_id " +
            "AND fp.entity_id = ld.entity_id " + 
            "AND (fy.id = :fiscalyear_id OR :fiscalyear_id is null) " + 
            "AND (fp.id = :fiscalperiod_id OR :fiscalperiod_id is null) " + 
            "ORDER BY ld.ledgerdate DESC, dt.doctype ASC, ld.documentnumber ASC").params(
                entity_id=entity_id, fiscalyear_id=fiscalyear_id, fiscalperiod_id=fiscalperiod_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0],
                            "documenttype_id":row[1],
                            "doctype":row[2],
                            "documentnumber":row[3],
                            "ledgerdate":row[4],
                            "fiscalyear":row[5],
                            "fiscalperiod":row[6],
                            "description":row[7],
                            "recorded_by":row[8],
                            "approved_by":row[9],
                            "entity_id":row[10]})
        return response

    @staticmethod
    def nextDocumentNumber(entity_id, documenttype_id):
        stmt = text("SELECT " +
            "COALESCE(MAX(ld.documentnumber), 0)+1 " +
            "FROM ledger_document ld " +
            "WHERE ld.entity_id = :entity_id " +
            "AND ld.documenttype_id = :documenttype_id ").params(
                entity_id=entity_id, documenttype_id=documenttype_id)
        res = db.engine.execute(stmt)

        newnum = -1
        for row in res:
            newnum = row[0]
        return newnum


class LedgerRow(Base):

    ledgerdocument_id = db.Column(db.Integer, db.ForeignKey("ledger_document.id"), nullable = False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    amount = db.Column(db.Integer, nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable = False)
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable = False)
    description = db.Column(db.String(255), nullable=False)
    recorded_by = db.Column(db.String(144), nullable = False)
    approved_by = db.Column(db.String(144), nullable = True)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    def __init__(self, ledgerdocument_id, account_id, amount,
                    activity_id, domain_id, description, recorded_by, entity_id):
        self.ledgerdocument_id = ledgerdocument_id
        self.account_id = account_id
        self.amount = amount
        self.activity_id = activity_id
        self.domain_id = domain_id
        self.description = description
        self.recorded_by = recorded_by
        self.entity_id = entity_id
