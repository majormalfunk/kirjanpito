from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.accountgroups.models import AccountGroup
from application.accountgroups.forms import AccountGroupForm, AccountGroupEditForm

@app.route("/accountgroupss", methods=["GET"])
def accountgroups_index():
    return render_template("accountgroups/list.html",
    accountgroups = AccountGroup.query.filter(AccountGroup.entity_id == current_user.get_entity_id()).order_by(AccountGroup.number).all())

@app.route("/accountgroups/new/")
def accountgroups_form():
    return render_template("accountgroups/new.html", form = AccountGroupForm())

@app.route("/accountgroups/select/<accountgroup_id>/", methods=["POST"])
@login_required
def accountgroup_select_for_edit(accountgroup_id):

    print("Valittu editoitavaksi tiliryhmä id = " + accountgroup_id)

    form = AccountGroupEditForm()
    accountgroup = AccountGroup.query.get(accountgroup_id)
    form.name.data = accountgroup.name
    form.description.data = accountgroup.description
    form.inuse.data = accountgroup.inuse

    return render_template("accountgroups/edit.html", form = form, accountgroup_id = accountgroup_id, number = accountgroup.number)

@app.route("/accountgroupss/edit/<accountgroup_id>/", methods=["POST"])
@login_required
def accountgroups_edit(accountgroup_id):

    print("Tehdään tiliryhmälle jotain")

    form = AccountGroupEditForm(request.form)

    if not form.validate():
        return render_template("accountgroups/edit.html", form = form, accountgroup_id = accountgroup_id)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        accountgroup = AccountGroup.query.get(accountgroup_id)
        accountgroup.name = form.name.data
        accountgroup.description = form.description.data
        accountgroup.inuse = form.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = AccountGroup.query.get(accountgroup_id)
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("accountgroups_index"))

@app.route("/accountgroups/", methods=["POST"])
@login_required
def accountgroups_create():
    form = AccountGroupForm(request.form)

    if not form.validate():
        return render_template("accountgroups/new.html", form = form)

    a = AccountGroup(form.number.data, form.name.data, form.description.data, form.inuse.data, current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        pass

    return redirect(url_for("accountgroups_index"))
