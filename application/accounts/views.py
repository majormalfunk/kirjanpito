from application import app, db
from flask import redirect, render_template, request, url_for
from application.accounts.models import Account

@app.route("/accounts", methods=["GET"])
def accounts_index():
    return render_template("accounts/list.html", accounts = Account.query.order_by(Account.code).all())

@app.route("/accounts/new/")
def accounts_form():
    return render_template("accounts/new.html")

@app.route("/accounts/<account_id>/", methods=["POST"])
def account_toggle_inuse(account_id):

    a = Account.query.get(account_id)
    u = request.form.get("inuse") == "True" 
    a.inuse = u
    db.session().commit()
  
    return redirect(url_for("accounts_index"))

@app.route("/accounts/", methods=["POST"])
def accounts_create():
    print(request.form.get("code"))
    print(request.form.get("name"))
    print(request.form.get("inuse"))  

    a = Account(request.form.get("code"), request.form.get("name"), request.form.get("inuse") == "True")
    db.session().add(a)
    db.session().commit()

    return redirect(url_for("accounts_index"))
