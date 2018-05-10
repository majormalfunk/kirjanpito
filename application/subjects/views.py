from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.activities.models import Activity
from application.activities.forms import ActivityForm
from application.domains.models import Domain
from application.domains.forms import DomainForm

##
## PERUSREITTI
##
@app.route("/subjects", methods=["GET", "POST"])
@login_required(role="admin")
def subjects_index():

    print("*** subjects_index ***")

    return render_template("subjects/list.html",
    action = "NoAction",
    targetactivity = -1,
    targetdomain = -1,
    subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
    newactivityform = ActivityForm(),
    newdomainform = DomainForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TOIMINTO
##
@app.route("/subjects/newactivity/", methods=["POST"])
@login_required(role="admin")
def activity_new_activity():

    activityform = ActivityForm(request.form)

    if not activityform.validate():
        print("Validointi ei onnistunut")
        return render_template("subjects/list.html",
            action = "FixNewActivity",
            targetactivity = -1,
            targetdomain = -1,
            subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
            fixnewactivityform = activityform,
            newactivityform = ActivityForm(),
            newdomainform = DomainForm())

    print("Yritetään tallentaa tietokantaan")

    a = Activity(activityform.orderer.data,
                    activityform.code.data,
                    activityform.name.data,
                    activityform.description.data,
                    activityform.inuse.data,
                    current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä toimintoa tietokantaan")
        pass

    return redirect(url_for("subjects_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TOIMINTO EDITOITAVAKSI
##
@app.route("/subjects/selectactivity/<activity_id>/", methods=["POST"])
@login_required(role="admin")
def activity_select_activity(activity_id):

    print("Valittu editoitavaksi toiminto id = " + activity_id)

    editactivityform = ActivityForm(request.form)
    activity = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
    editactivityform.id.data = activity.id
    editactivityform.orderer.data = activity.orderer
    editactivityform.code.data = activity.code
    editactivityform.name.data = activity.name
    editactivityform.description.data = activity.description
    editactivityform.inuse.data = activity.inuse

    return render_template("subjects/list.html",
        action = "EditActivity",
        targetactivity = activity_id,
        targetdomain = -1,
        subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
        newactivityform = ActivityForm(),
        editactivityform = editactivityform,
        newdomainform = DomainForm())

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TOIMINTOON
##
@app.route("/subjects/editactivity/<activity_id>/", methods=["POST"])
@login_required(role="admin")
def activity_edit_activity(activity_id):

    print("Tehdään tiliryhmälle " + activity_id + " jotain")

    editactivityform = ActivityForm(request.form)
    print("activityid on " + str(editactivityform.id.data))
    editactivityform.id.data = activity_id

    if not editactivityform.validate():
        return render_template("subjects/list.html",
            action = "EditActivity",
            targetactivity = activity_id,
            targetdomain = -1,
            subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
            newactivityform = ActivityForm(),
            editactivityform = editactivityform,
            newdomainform = DomainForm())

    if "action_update" in request.form:
        print("Yritetään tallentaa muutettua toimintoa")
        activity = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
        activity.name = editactivityform.name.data
        activity.description = editactivityform.description.data
        activity.inuse = editactivityform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa toimintoa")
        obsolete = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("subjects_index"))

##
## TÄMÄ REITTI, KUN OLLAAN LISÄÄMÄSSÄ UUTTA KUSTANNUSPAIKKAA
##
@app.route("/subjects/newdomain/<activity_id>/", methods=["POST"])
@login_required(role="admin")
def activity_new_domain(activity_id):

    domainform = DomainForm(request.form)
    print("Yritetään lisätä uutta kustannuspaikkaa toimintoon " + str(domainform.activity_id.data))

    if not domainform.validate():
        return render_template("subjects/list.html",
            action = "FixNewDomain",
            targetactivity = activity_id,
            targetdomain = -1,
            subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
            newactivityform = ActivityForm(),
            fixnewdomainform = domainform,
            newdomainform = DomainForm())


    a = Domain(domainform.orderer.data,
                domainform.code.data,
                domainform.name.data,
                domainform.description.data,
                domainform.inuse.data,
                activity_id,
                current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisätessä uutta kustannuspaikkaa tietokantaan")
        pass

    return redirect(url_for("subjects_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU KUSTANNUSPAIKKA EDITOITAVAKSI
##
@app.route("/subjects/selectdomain/<domain_id>/", methods=["POST"])
@login_required(role="admin")
def activity_select_domain(domain_id):

    print("Valittu editoitavaksi kustannuspaikka id = " + domain_id)

    editdomainform = DomainForm(request.form)
    domain = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
    editdomainform.id.data = domain_id
    editdomainform.orderer.data = domain.orderer
    editdomainform.code.data = domain.code
    editdomainform.name.data = domain.name
    editdomainform.description.data = domain.description
    editdomainform.inuse.data = domain.inuse

    return render_template("subjects/list.html",
        action = "EditDomain",
        targetactivity = domain.activity_id,
        targetdomain = domain_id,
        subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
        newactivityform = ActivityForm(),
        newdomainform = DomainForm(),
        editdomainform = editdomainform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA KUSTANNUSPAIKKAAN
##
@app.route("/subjects/editdomain/<domain_id>/", methods=["POST"])
@login_required(role="admin")
def activity_edit_domain(domain_id):

    print("Tehdään kustannuspaikalle jotain")

    editdomainform = DomainForm(request.form)

    print("id:", editdomainform.id.data)
    print("activity_id:", editdomainform.activity_id.data)

    if not editdomainform.validate():
        print("Kustannuspaikan validointi editoidessa ei onnistunut")
        return render_template("subjects/list.html",
            action = "EditDomain",
            targetactivity = editdomainform.activity_id.data,
            targetdomain = domain_id,
            subjects = Activity.findAllActivitiesAndDomains(current_user.get_entity_id()),
            newactivityform = ActivityForm(),
            newdomainform = DomainForm(),
            editdomainform = editdomainform)

    if "action_update" in request.form:
        print("Yritetään tallentaa muutettua kustannuspaikkaa")
        domain = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
        domain.name = editdomainform.name.data
        domain.description = editdomainform.description.data
        domain.inuse = editdomainform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa kustannuspaikkaa")
        obsolete = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("subjects_index"))



