from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.activities.models import Activity
from application.activities.forms import ActivityForm

##
## PERUSREITTI
##
@app.route("/activities", methods=["GET", "POST"])
@login_required(role="admin")
def activities_index():

    print("*** activities_index ***")

    return render_template("activities/list.html",
    action = "NoAction",
    targetactivity = -1,
    activities = Activity.query.filter(Activity.entity_id == current_user.get_entity_id()).order_by(Activity.orderer),
    newactivityform = ActivityForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TOIMINTO
##
@app.route("/activities/newactivity/", methods=["POST"])
@login_required(role="admin")
def activity_new_activity():

    activityform = ActivityForm(request.form)

    if not activityform.validate():
        print("Validointi ei onnistunut")
        return render_template("activities/list.html",
            action = "FixNewActivity",
            targetactivity = -1,
            activities = Activity.query.filter(Activity.entity_id == current_user.get_entity_id()).order_by(Activity.orderer),
            fixnewactivityform = activityform,
            newactivityform = ActivityForm())

    print("Yritetään tallentaa tietokantaan")

    a = Activity(activityform.code.data,
                activityform.orderer.data,
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

    return redirect(url_for("activities_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TOIMINTO EDITOITAVAKSI
##
@app.route("/activities/selectactivity/<activity_id>/", methods=["POST"])
@login_required(role="admin")
def activity_select_activity(activity_id):

    print("Valittu editoitavaksi toiminto id = " + activity_id)

    editactivityform = ActivityForm(request.form)
    activity = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
    editactivityform.id.data = activity.id
    editactivityform.code.data = activity.code
    editactivityform.orderer.data = activity.orderer
    editactivityform.name.data = activity.name
    editactivityform.description.data = activity.description
    editactivityform.inuse.data = activity.inuse

    return render_template("activities/list.html",
        action = "EditActivity",
        targetactivity = activity_id,
        activities = Activity.query.filter(Activity.entity_id == current_user.get_entity_id()).order_by(Activity.orderer),
        newactivityform = ActivityForm(),
        editactivityform = editactivityform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TOIMINTOON
##
@app.route("/activities/editactivity/<activity_id>/", methods=["POST"])
@login_required(role="admin")
def activity_edit_activity(activity_id):

    print("Tehdään toiminnolle " + activity_id + " jotain")

    editactivityform = ActivityForm(request.form)
    print("activityid on " + str(editactivityform.id.data))
    editactivityform.id.data = activity_id

    if not editactivityform.validate():
        return render_template("activities/list.html",
            action = "EditActivity",
            targetactivity = activity_id,
            activities = Activity.query.filter(Activity.entity_id == current_user.get_entity_id()).order_by(Activity.orderer),
            newactivityform = ActivityForm(),
            editactivityform = editactivityform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        activity = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
        activity.orderer = editactivityform.orderer.data
        activity.name = editactivityform.name.data
        activity.description = editactivityform.description.data
        activity.inuse = editactivityform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = Activity.query.filter(Activity.entity_id == current_user.get_entity_id(), Activity.id == activity_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("activities_index"))

