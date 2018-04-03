from flask import redirect, render_template, request, url_for

from application import app, db
from application.accounts.models import Account
from application.accounts.forms import AccountForm, AccountEditForm

@app.route("/accounts", methods=["GET"])
def accounts_index():
    return render_template("accounts/list.html", accounts = Account.query.order_by(Account.code).all())

@app.route("/accounts/new/")
def accounts_form():
    return render_template("accounts/new.html", form = AccountForm())

@app.route("/accounts/<account_id>/", methods=["POST"])
def account_toggle_inuse(account_id):

    a = Account.query.get(account_id)
    u = request.form.get("inuse") == "True" 
    a.inuse = u
    db.session().commit()
  
    return redirect(url_for("accounts_index"))

@app.route("/accounts/select/<account_id>/", methods=["POST"])
def account_select_for_edit(account_id):

    print("Valittu editoitavaksi " + account_id)

    form = AccountEditForm()
    account = Account.query.get(account_id)
    ##form.code.data = account.code
    form.name.data = account.name
    form.description.data = account.description
    form.inuse.data = account.inuse

    return render_template("accounts/edit.html", form = form, account_id = account_id, code = account.code)

@app.route("/accounts/edit/<account_id>/", methods=["POST"])
def accounts_edit(account_id):

    print("Yritetään tallentaa")

    form = AccountEditForm(request.form)

    if not form.validate():
        return render_template("accounts/edit.html", form = form, account_id = account_id)

    account = Account.query.get(account_id)
    account.name = form.name.data
    account.description = form.description.data
    account.inuse = form.inuse.data
    db.session().commit()

    return redirect(url_for("accounts_index"))

@app.route("/accounts/", methods=["POST"])
def accounts_create():
    form = AccountForm(request.form)

    if not form.validate():
        return render_template("accounts/new.html", form = form)

    a = Account(form.code.data, form.name.data, form.description.data, form.inuse.data)
    db.session().add(a)
    db.session().commit()

    return redirect(url_for("accounts_index"))
