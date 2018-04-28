from application import db
from application.models import TimeBased
from sqlalchemy import UniqueConstraint, text

class FiscalYear(TimeBased):

    name = db.Column(db.String(4), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    fiscalperiods = db.relationship("FiscalPeriod", backref='fiscalyear_fiscalperiods', lazy=True)

    __table_args__ = (UniqueConstraint('name', 'entity_id', name='fiscalyear_entity_uc'),)

    def __init__(self, name, startdate, enddate, closed, locked, entity_id):
        self.name = name
        self.startdate = startdate
        self.enddate = enddate
        self.closed = closed
        self.locked = locked
        self.entity_id = entity_id

    @staticmethod
    def findAllFiscalYearsAndPeriods(entity_id):
        stmt = text("SELECT " +
            "fy.id, fy.name, fy.startdate, fy.enddate, fy.closed, fy.locked, " +
            "fp.id, fp.name, fp.startdate, fp.enddate, fp.closed, fp.locked " +
            "FROM fiscal_year fy " +
            "LEFT JOIN fiscal_period fp on fy.id = fp.fiscalyear_id " +
            "WHERE fy.entity_id = :entity_id " +
            "ORDER BY fy.enddate DESC, fp.enddate DESC").params(entity_id=entity_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"fiscal_year_id":row[0],
                            "fiscal_year_name":row[1],
                            "fiscal_year_startdate":row[2],
                            "fiscal_year_enddate":row[3],
                            "fiscal_year_closed":row[4],
                            "fiscal_year_locked":row[5],
                            "fiscal_period_id":row[6],
                            "fiscal_period_name":row[7],
                            "fiscal_period_startdate":row[8],
                            "fiscal_period_enddate":row[9],
                            "fiscal_period_closed":row[10],
                            "fiscal_period_locked":row[11]})
        return response

class FiscalPeriod(TimeBased):

    name = db.Column(db.String(6), nullable=False)
    fiscalyear_id = db.Column(db.Integer, db.ForeignKey("fiscal_year.id"), nullable = False)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable = False)

    __table_args__ = (UniqueConstraint('name', 'entity_id', name='fiscalperiod_entity_uc'),)

    def __init__(self, name, startdate, enddate, closed, locked, fiscalyear_id, entity_id):
        self.name = name
        self.startdate = startdate
        self.enddate = enddate
        self.closed = closed
        self.locked = locked
        self.fiscalyear_id = fiscalyear_id
        self.entity_id = entity_id
