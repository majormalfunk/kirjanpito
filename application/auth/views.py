from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from passlib.hash import pbkdf2_sha256

from application import app, db, login_required
from application.auth.models import UserAccount
from application.auth.forms import LoginForm, RegisterForm, UserAccountForm, EditUserAccountForm
from application.entity.models import Entity

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

    ## Luodaan yhteisö, jolle käyttäjä rekisteröidään

    hshpwd = pbkdf2_sha256.hash(form.password.data)

    ##print("Häsätty :" + hshpwd)

    ent = Entity(code="", name="", description="")
    db.session().add(ent)
    db.session().flush()
    print("Entity id = " + str(ent.id))

    try:
        newuser = UserAccount(
            username=form.username.data,
            password=hshpwd,
            name=form.name.data,
            entity_id = ent.id,
            role = "admin")
        db.session().add(newuser)
        db.session().commit()
        print("Käyttäjä " + newuser.name + " rekisteröitiin")
    except:
        db.session().rollback()
        db.session().delete(ent)
        pass

    user = UserAccount.query.filter_by(username=form.username.data, password=hshpwd).first()
    if not user:
        return render_template("auth/registerform.html", form = form,
                               error = "Jokin meni pieleen rekisteröitymisessä")

    login_user(user)
    return redirect(url_for("index"))


##
## Kirjautuminen
##
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    try:
        user = UserAccount.query.filter_by(username=form.username.data).first()
        if not pbkdf2_sha256.verify(form.password.data, user.password):
            return render_template("auth/loginform.html", form = form,
                               error = "Väärä käyttäjätunnus tai salasana")
    except:
        return render_template("auth/loginform.html", form = LoginForm(),
                               error = "Väärä käyttäjätunnus tai salasana")

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

########################## 
#### KÄYTTÄJÄHALLINTA ####
########################## 

##
## PERUSREITTI
##
@app.route("/useraccounts", methods=["GET", "POST"])
@login_required(role="admin")
def useraccounts_index():

    print("*** useraccounts_index ***")

    return render_template("auth/list.html",
    action = "NoAction",
    targetuseraccount = -1,
    useraccounts = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id()).order_by(UserAccount.name),
    newuseraccountform = UserAccountForm())


##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI KÄYTTÄJÄ
##
@app.route("/useraccounts/newuseraccount/", methods=["POST"])
@login_required(role="admin")
def useraccount_new_useraccount():

    useraccountform = UserAccountForm(request.form)

    if not useraccountform.validate():
        print("Validointi ei onnistunut")
        return render_template("auth/list.html",
            action = "FixNewUserAccount",
            targetuseraccount = -1,
            useraccounts = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id()).order_by(UserAccount.name),
            fixnewuseraccountform = useraccountform,
            newuseraccountform = UserAccountForm())

    print("Yritetään tallentaa tietokantaan")

    ## name, username, password, entity_id, role

    hshpwd = pbkdf2_sha256.hash(useraccountform.password.data)

    useraccount = UserAccount(useraccountform.name.data,
                useraccountform.username.data,
                hshpwd,
                current_user.get_entity_id(),
                useraccountform.role.data)
    #try:
    db.session().add(useraccount)
    db.session().commit()
    #    print("Tallennus onnistui")
    #except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
    #    print("Tapahtui virhe lisättäessä käyttäjää tietokantaan")
    #    pass

    return redirect(url_for("useraccounts_index"))


##
## TÄMÄ REITTI, KUN ON VALITTU KÄYTTÄJÄ EDITOITAVAKSI
##
@app.route("/useraccounts/selectuseraccount/<useraccount_id>/", methods=["POST"])
@login_required(role="admin")
def useraccount_select_useraccount(useraccount_id):

    edituseraccountform = EditUserAccountForm(request.form)
    useraccount = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id(), UserAccount.id == useraccount_id).first()
    
    edituseraccountform.id.data = useraccount.id
    edituseraccountform.name.data = useraccount.name
    edituseraccountform.username.data = useraccount.username
    edituseraccountform.role.data = useraccount.role

    return render_template("auth/list.html",
        action = "EditUserAccount",
        targetuseraccount = useraccount_id,
        useraccounts = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id()).order_by(UserAccount.name),
        newuseraccountform = UserAccountForm(),
        edituseraccountform = edituseraccountform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA KÄYTTÄJÄÄN
##
@app.route("/useraccounts/edituseraccount/<useraccount_id>/", methods=["POST"])
@login_required(role="admin")
def useraccount_edit_useraccount(useraccount_id):

    edituseraccountform = EditUserAccountForm(request.form)
    edituseraccountform.id.data = useraccount_id
    edituseraccountform.username.data = current_user.get_username()

    if not edituseraccountform.validate():
        print("Validointi ei onnistunut")
        return render_template("auth/list.html",
            action = "EditUserAccount",
            targetuseraccount = useraccount_id,
            useraccounts = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id()).order_by(UserAccount.name),
            newuseraccountform = UserAccountForm(),
            edituseraccountform = edituseraccountform)

    adminCount = UserAccount.adminCount(current_user.get_entity_id())

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        useraccount = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id(), UserAccount.id == useraccount_id).first()

        if (adminCount > 1 or useraccount.role != "admin"):
            useraccount.role = edituseraccountform.role.data
        useraccount.name = edituseraccountform.name.data

        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")

        if (adminCount > 1) :
            obsolete = UserAccount.query.filter(UserAccount.entity_id == current_user.get_entity_id(), UserAccount.id == useraccount_id).first()
            try:
                db.session().delete(obsolete)
                db.session.commit()
            except:
                ## TÄHÄN VIRHETILANTEEN KÄSITTELY
                pass

    return redirect(url_for("useraccounts_index"))
