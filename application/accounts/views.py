from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.accounts.models import Account
from application.accountgroups.models import AccountGroup
from application.accounts.forms import AccountForm, AccountEditForm

@app.route("/accounts", methods=["GET"])
def accounts_index():

    return render_template("accounts/list.html",
    accounts = Account.query.filter(Account.entity_id == current_user.get_entity_id()).order_by(Account.number).all())

@app.route("/accounts/new/<accountgroup_id>/", methods=["GET", "POST"])
@login_required(role="admin")
def accounts_form(accountgroup_id):

    accountgroup = AccountGroup.query.filter(AccountGroup.entity_id == current_user.get_entity_id(), AccountGroup.id == accountgroup_id).first()

    return render_template("accounts/new.html", form = AccountForm(), accountgroup = accountgroup)
    

@app.route("/accounts/select/<account_id>/", methods=["POST"])
@login_required(role="admin")
def account_select_for_edit(account_id):

    print("Valittu editoitavaksi tili id = " + account_id)

    form = AccountEditForm()
    account = Account.query.get(account_id)
    form.name.data = account.name
    form.description.data = account.description
    form.inuse.data = account.inuse

    return redirect(url_for("accountgroups_edit_account",
        editAccountForm = form, editAccountId = account_id, editAccountNumber = account.number), code=307)
    ##return render_template("accounts/edit.html", form = form, account_id = account_id, number = account.number)

@app.route("/accounts/edit/<account_id>/", methods=["POST"])
@login_required(role="admin")
def accounts_edit(account_id):

    print("Tehdään tilille jotain")

    form = AccountEditForm(request.form)
    account = Account.query.get(account_id)

    if not form.validate():
        return redirect(url_for("accountgroups_edit_account",
            editAccountForm = form, editAccountId = account_id, editAccountNumber = account.number), code=307)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        account.name = form.name.data
        account.description = form.description.data
        account.inuse = form.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = Account.query.get(account_id)
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("accountgroups_index"))

@app.route("/accounts/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
def accounts_create(accountgroup_id):
    form = AccountForm(request.form)

    if not form.validate():
        print("Validointi ei onnistunut accounts_create:ssa")
        return redirect(url_for("accountgroups_new_account", form = form, accountgroup = accountgroup_id), code=307)

    a = Account(form.number.data, form.name.data, form.description.data, form.inuse.data, accountgroup_id, current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        pass

    return redirect(url_for("accountgroups_index"))
