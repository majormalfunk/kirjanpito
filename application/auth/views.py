from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import UserAccount
from application.auth.forms import LoginForm, RegisterForm

#
# Rekisteröityminen
#
@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)
    # mahdolliset validoinnit
    
    print("Yritetään rekisteröitymistä")
    if not form.validate():
        return render_template("auth/registerform.html", form = form)

    testuser = UserAccount.query.filter_by(username=form.username.data).first()
    if testuser:
        varattu = form.username.data
        form.username.data = ""
        return render_template("auth/registerform.html", form = form,
                               error = "Käyttäjätunnus " + varattu + " on jo käytössä")

    newuser = UserAccount(username=form.username.data, password=form.password.data, name=form.name.data)
    db.session().add(newuser)
    db.session().commit()
    print("Käyttäjä " + newuser.name + " rekisteröitiin")

    user = UserAccount.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/registerform.html", form = form,
                               error = "Jokin meni pieleen rekisteröitymisessä")

    login_user(user)
    return redirect(url_for("index"))


    ##loginForm = LoginForm()
    ##loginForm.username = newuser.username
    ##loginForm.password = newuser.password

    ##return redirect(url_for("accounts_index", form = loginForm))

##
## Kirjautuminen
##
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = UserAccount.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "V&auml;&auml;r&auml; k&auml;ytt&auml;j&auml;tunnus tai salasana")


    print("Käyttäjä " + user.name + " tunnistettiin")
    login_user(user)
    return redirect(url_for("index"))

##
## Uloskirjautuminen
##
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 