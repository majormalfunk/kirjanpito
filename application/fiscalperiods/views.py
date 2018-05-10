from datetime import timedelta
from datetime import date

from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.fiscalperiods.models import FiscalYear, FiscalPeriod
from application.fiscalperiods.forms import FiscalYearForm, FiscalPeriodForm

##
## PERUSREITTI
##
@app.route("/fiscalperiods", methods=["GET", "POST"])
@login_required(role="admin")
def fiscalperiods_index():

    print("*** fiscalperiods_index ***")

    return render_template("fiscalperiods/list.html",
    action = "NoAction",
    targetyear = -1,
    targetperiod = -1,
    fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
    newfiscalyearform = FiscalYearForm(),
    newfiscalperiodform = FiscalPeriodForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TILIKAUSI
##
@app.route("/fiscalperiods/newyear/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_new_year():

    fiscalyearform = FiscalYearForm(request.form)

    if not fiscalyearform.validate():
        print("Validointi ei onnistunut")
        print("Alkupvm: ", fiscalyearform.startdate)
        print("Loppupvm: ", fiscalyearform.enddate)
        return render_template("fiscalperiods/list.html",
            action = "FixNewFiscalYear",
            targetyear = -1,
            targetperiod = -1,
            fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
            fixnewfiscalyearform = fiscalyearform,
            newfiscalyearform = FiscalYearForm(),
            newfiscalperiodform = FiscalPeriodForm())

    print("Yritetään tallentaa tietokantaan")

    newyear = FiscalYear(fiscalyearform.name.data,
                    fiscalyearform.startdate.data,
                    fiscalyearform.enddate.data,
                    fiscalyearform.closed.data,
                    fiscalyearform.locked.data,
                    current_user.get_entity_id())
    try:
        db.session().add(newyear)
        db.session().commit()
        print("Tilikauden " + newyear.name + " tallennus onnistui")

    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä tilikautta tietokantaan")
        pass

    ## LISÄTÄÄN TILIKAUDELLE OLETUSJAKSOT
    periodstart = newyear.startdate
    periodend = newyear.enddate
    for p in range(newyear.startdate.month, newyear.enddate.month+1):
        periodname = str(p)
        periodstart = date(newyear.startdate.year, p, 1)
        if p == 12:
            periodend = newyear.enddate
        else:
            periodtemp = date(newyear.startdate.year, p+1, 1)
            periodend = periodtemp + timedelta(-1)
        if p < 10:
            periodname = "0" + periodname
        periodname = newyear.name + periodname
        ##print(periodname + " : " + str(periodstart) + " -> " + str(periodend))
        newperiod = FiscalPeriod(periodname,
                periodstart,
                periodend,
                newyear.closed,
                newyear.locked,
                newyear.id,
                current_user.get_entity_id())

        try:
            db.session().add(newperiod)
            db.session().commit()
            print("Jakson " + newperiod.name + " tallennus onnistui")

        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            print("Tapahtui virhe lisättäessä tilikautta tietokantaan")
            pass

    return redirect(url_for("fiscalperiods_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TILIKAUSI EDITOITAVAKSI
##
@app.route("/fiscalperiods/selectyear/<fiscalyear_id>/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_select_year(fiscalyear_id):

    print("Valittu editoitavaksi tilikausi id = " + fiscalyear_id)

    editfiscalyearform = FiscalYearForm(request.form)
    fiscalyear = FiscalYear.query.filter(FiscalYear.entity_id == current_user.get_entity_id(), FiscalYear.id == fiscalyear_id).first()
    editfiscalyearform.id.data = fiscalyear.id
    editfiscalyearform.name.data = fiscalyear.name
    editfiscalyearform.startdate.data = fiscalyear.startdate
    editfiscalyearform.enddate.data = fiscalyear.enddate
    editfiscalyearform.closed.data = fiscalyear.closed
    editfiscalyearform.locked.data = fiscalyear.locked

    return render_template("fiscalperiods/list.html",
        action = "EditFiscalYear",
        targetyear = fiscalyear_id,
        targetperiod = -1,
        fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
        newfiscalyearform = FiscalYearForm(),
        editfiscalyearform = editfiscalyearform,
        newfiscalperiodform = FiscalPeriodForm())

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TILIKAUTEEN
##
@app.route("/fiscalperiods/edityear/<fiscalyear_id>/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_edit_year(fiscalyear_id):

    print("Tehdään tilikaudelle " + fiscalyear_id + " jotain")

    editfiscalyearform = FiscalYearForm(request.form)
    print("yearid on " + str(editfiscalyearform.id.data))
    editfiscalyearform.id.data = fiscalyear_id

    if not editfiscalyearform.validate():
        return render_template("fiscalperiods/list.html",
            action = "EditFiscalYear",
            targetyear = fiscalyear_id,
            targetperiod = -1,
            fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
            newfiscalyearform = FiscalYearForm(),
            editfiscalyearform = editfiscalyearform,
            newfiscalperiodform = FiscalPeriodForm())

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        fiscalyear = FiscalYear.query.filter(FiscalYear.entity_id == current_user.get_entity_id(), FiscalYear.id == fiscalyear_id).first()
        fiscalyear.name = editfiscalyearform.name.data
        fiscalyear.startdate = editfiscalyearform.startdate.data
        fiscalyear.enddate = editfiscalyearform.enddate.data
        fiscalyear.closed = editfiscalyearform.closed.data
        fiscalyear.locked = editfiscalyearform.locked.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = FiscalYear.query.filter(FiscalYear.entity_id == current_user.get_entity_id(), FiscalYear.id == fiscalyear_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("fiscalperiods_index"))

##
## TÄMÄ REITTI, KUN OLLAAN LISÄÄMÄSSÄ UUTTA KAUTTA
##
@app.route("/fiscalperiod/newperiod/<fiscalyear_id>/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_new_period(fiscalyear_id):

    fiscalperiodform = FiscalPeriodForm(request.form)
    print("Yritetään lisätä uutta kautta tilikauteen " + str(fiscalperiodform.fiscalyear_id.data))

    if not fiscalperiodform.validate():
        print("Lisääminen ei onnistunut")
        return render_template("fiscalperiods/list.html",
            action = "FixNewFiscalPeriod",
            targetyear = fiscalyear_id,
            targetperiod = -1,
            fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
            newfiscalyearform = FiscalYearForm(),
            fixnewfiscalperiodform = fiscalperiodform,
            newfiscalperiodform = FiscalPeriodForm())

    period = FiscalPeriod(fiscalperiodform.name.data,
                    fiscalperiodform.startdate.data,
                    fiscalperiodform.enddate.data,
                    fiscalperiodform.closed.data,
                    fiscalperiodform.locked.data,
                    fiscalperiodform.fiscalyear_id.data,
                    current_user.get_entity_id())
    try:
        db.session().add(period)
        db.session().commit()
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisätessä uutta kautta tietokantaan")
        pass

    return redirect(url_for("fiscalperiods_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU KAUSI EDITOITAVAKSI
##
@app.route("/fiscalperiods/selectperiod/<fiscalperiod_id>/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_select_period(fiscalperiod_id):

    print("Valittu editoitavaksi kausi id = " + fiscalperiod_id)

    editfiscalperiodform = FiscalPeriodForm(request.form)
    fiscalperiod = FiscalPeriod.query.filter(FiscalPeriod.entity_id == current_user.get_entity_id(), FiscalPeriod.id == fiscalperiod_id).first()
    editfiscalperiodform.id.data = fiscalperiod_id
    editfiscalperiodform.name.data = fiscalperiod.name
    editfiscalperiodform.startdate.data = fiscalperiod.startdate
    editfiscalperiodform.enddate.data = fiscalperiod.enddate
    editfiscalperiodform.closed.data = fiscalperiod.closed
    editfiscalperiodform.locked.data = fiscalperiod.locked

    return render_template("fiscalperiods/list.html",
        action = "EditFiscalPeriod",
        targetyear = fiscalperiod.fiscalyear_id,
        targetperiod = fiscalperiod_id,
        fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
        newfiscalyearform = FiscalYearForm(),
        newfiscalperiodform = FiscalPeriodForm(),
        editfiscalperiodform = editfiscalperiodform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA KAUTEEN
##
@app.route("/fiscalperiods/editperiod/<fiscalperiod_id>/", methods=["POST"])
@login_required(role="admin")
def fiscalperiod_edit_period(fiscalperiod_id):

    print("Tehdään kaudelle jotain")

    editfiscalperiodform = FiscalPeriodForm(request.form)

    print("id:", editfiscalperiodform.id.data)
    print("year_id:", editfiscalperiodform.fiscalyear_id.data)

    if not editfiscalperiodform.validate():
        print("Kauden validointi editoidessa ei onnistunut")
        return render_template("fiscalperiods/list.html",
            action = "EditFiscalPeriod",
            targetyear = editfiscalperiodform.fiscalyear_id.data,
            targetperiod = fiscalperiod_id,
            fiscalperiods = FiscalYear.findAllFiscalYearsAndPeriods(current_user.get_entity_id()),
            newfiscalyearform = FiscalYearForm(),
            newfiscalperiodform = FiscalPeriodForm(),
            editfiscalperiodform = editfiscalperiodform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        fiscalperiod = FiscalPeriod.query.filter(FiscalPeriod.entity_id == current_user.get_entity_id(), FiscalPeriod.id == fiscalperiod_id).first()
        fiscalperiod.name = editfiscalperiodform.name.data
        fiscalperiod.startdate = editfiscalperiodform.startdate.data
        fiscalperiod.enddate = editfiscalperiodform.enddate.data
        fiscalperiod.closed = editfiscalperiodform.closed.data
        fiscalperiod.locked = editfiscalperiodform.locked.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = FiscalPeriod.query.filter(FiscalPeriod.entity_id == current_user.get_entity_id(), FiscalPeriod.id == fiscalperiod_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("fiscalperiods_index"))



