from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.accountgroups.models import AccountGroup
from application.accountgroups.forms import AccountGroupForm, AccountGroupEditForm
from application.accounts.models import Account
from application.accounts.forms import AccountForm, AccountEditForm

@app.route("/accountgroups", methods=["GET"])
@login_required(role="admin")
def accountgroups_index():

    print("*** accountgroups_index ***")

    return render_template("accountgroups/list.html",
    accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
    newaccountgroupform = AccountGroupForm(),
    newaccountform = AccountForm())

@app.route("/accountgroups", methods=["POST"])
@login_required(role="admin")
def accountgroups_edit_account():

    print("*** accountgroups_edit_account ***")

    editaccountid = request.args.get("editAccountId")
    editaccountnumber = request.args.get("editAccountNumber")
    editaccountform = AccountEditForm()
    account = Account.query.get(editaccountid)
    editaccountform.name.data = account.name
    editaccountform.description.data = account.description
    editaccountform.inuse.data = account.inuse
    editaccountform.accountgroup = account.accountgroup_id

    return render_template("accountgroups/list.html",
    accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
    newaccountgroupform = AccountGroupForm(),
    newaccountform = AccountForm(),
    editaccountform = editaccountform,
    editaccountid = editaccountid,
    editaccountnumber = editaccountnumber)

@app.route("/accountgroups/new/")
@login_required(role="admin")
def accountgroups_form():
    return render_template("accountgroups/new.html", form = AccountGroupForm())

@app.route("/accountgroups/select/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_select_for_edit(accountgroup_id):

    print("Valittu editoitavaksi tiliryhmä id = " + accountgroup_id)

    form = AccountGroupEditForm()
    accountgroup = AccountGroup.query.get(accountgroup_id)
    form.name.data = accountgroup.name
    form.description.data = accountgroup.description
    form.inuse.data = accountgroup.inuse

    return render_template("accountgroups/edit.html", form = form, accountgroup_id = accountgroup_id, number = accountgroup.number)

@app.route("/accountgroupss/edit/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
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
@login_required(role="admin")
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
