from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.accountgroups.models import AccountGroup
from application.accountgroups.forms import AccountGroupForm
from application.accounts.models import Account
from application.accounts.forms import AccountForm

##
## PERUSREITTI
##
@app.route("/accountgroups", methods=["GET", "POST"])
@login_required(role="admin")
def accountgroups_index():

    print("*** accountgroups_index ***")

    return render_template("accountgroups/list.html",
    action = "NoAction",
    targetgroup = -1,
    targetaccount = -1,
    accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
    newaccountgroupform = AccountGroupForm(),
    newaccountform = AccountForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TILIRYHMÄ
##
@app.route("/accountgroups/newgroup/", methods=["POST"])
@login_required(role="admin")
def accountgroup_new_group():

    accountgroupform = AccountGroupForm(request.form)

    if not accountgroupform.validate():
        print("Validointi ei onnistunut")
        return render_template("accountgroups/list.html",
            action = "FixNewAccountGroup",
            targetgroup = -1,
            targetaccount = -1,
            accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
            fixnewaccountgroupform = accountgroupform,
            newaccountgroupform = AccountGroupForm(),
            newaccountform = AccountForm())

    print("Yritetään tallentaa tietokantaan")

    a = AccountGroup(accountgroupform.number.data,
                    accountgroupform.name.data,
                    accountgroupform.description.data,
                    accountgroupform.inuse.data,
                    current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä tiliryhmää tietokantaan")
        pass

    return redirect(url_for("accountgroups_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TILIRYHMÄ EDITOITAVAKSI
##
@app.route("/accountgroups/selectgroup/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_select_group(accountgroup_id):

    print("Valittu editoitavaksi tiliryhmä id = " + accountgroup_id)

    editaccountgroupform = AccountGroupForm(request.form)
    accountgroup = AccountGroup.query.filter(AccountGroup.entity_id == current_user.get_entity_id(), AccountGroup.id == accountgroup_id).first()
    editaccountgroupform.id.data = accountgroup.id
    editaccountgroupform.number.data = accountgroup.number
    editaccountgroupform.name.data = accountgroup.name
    editaccountgroupform.description.data = accountgroup.description
    editaccountgroupform.inuse.data = accountgroup.inuse

    return render_template("accountgroups/list.html",
        action = "EditAccountGroup",
        targetgroup = accountgroup_id,
        targetaccount = -1,
        accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
        newaccountgroupform = AccountGroupForm(),
        editaccountgroupform = editaccountgroupform,
        newaccountform = AccountForm())

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TILIRYHMÄÄN
##
@app.route("/accountgroups/editgroup/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_edit_group(accountgroup_id):

    print("Tehdään tiliryhmälle " + accountgroup_id + " jotain")

    editaccountgroupform = AccountGroupForm(request.form)
    print("groupid on " + str(editaccountgroupform.id.data))
    editaccountgroupform.id.data = accountgroup_id

    if not editaccountgroupform.validate():
        return render_template("accountgroups/list.html",
            action = "EditAccountGroup",
            targetgroup = accountgroup_id,
            targetaccount = -1,
            accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
            newaccountgroupform = AccountGroupForm(),
            editaccountgroupform = editaccountgroupform,
            newaccountform = AccountForm())

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        accountgroup = AccountGroup.query.filter(AccountGroup.entity_id == current_user.get_entity_id(), AccountGroup.id == accountgroup_id).first()
        accountgroup.name = editaccountgroupform.name.data
        accountgroup.description = editaccountgroupform.description.data
        accountgroup.inuse = editaccountgroupform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = AccountGroup.query.filter(AccountGroup.entity_id == current_user.get_entity_id(), AccountGroup.id == accountgroup_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("accountgroups_index"))

##
## TÄMÄ REITTI, KUN OLLAAN LISÄÄMÄSSÄ UUTTA TILIÄ
##
@app.route("/accountgroups/newaccount/<accountgroup_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_new_account(accountgroup_id):

    accountform = AccountForm(request.form)
    print("Yritetään lisätä uutta tiliä ryhmään " + str(accountform.accountgroup_id.data))

    if not accountform.validate():
        return render_template("accountgroups/list.html",
            action = "FixNewAccount",
            targetgroup = accountgroup_id,
            targetaccount = -1,
            accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
            newaccountgroupform = AccountGroupForm(),
            fixnewaccountform = accountform,
            newaccountform = AccountForm())


    a = Account(accountform.number.data, accountform.name.data, accountform.description.data, accountform.inuse.data, accountgroup_id, current_user.get_entity_id())
    try:
        db.session().add(a)
        db.session().commit()
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisätessä uutta tiliä tietokantaan")
        pass

    return redirect(url_for("accountgroups_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TILI EDITOITAVAKSI
##
@app.route("/accountgroups/selectaccount/<account_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_select_account(account_id):

    print("Valittu editoitavaksi tili id = " + account_id)

    editaccountform = AccountForm(request.form)
    account = Account.query.filter(Account.entity_id == current_user.get_entity_id(), Account.id == account_id).first()
    editaccountform.id.data = account_id
    editaccountform.number.data = account.number
    editaccountform.name.data = account.name
    editaccountform.description.data = account.description
    editaccountform.inuse.data = account.inuse

    return render_template("accountgroups/list.html",
        action = "EditAccount",
        targetgroup = account.accountgroup_id,
        targetaccount = account_id,
        accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
        newaccountgroupform = AccountGroupForm(),
        newaccountform = AccountForm(),
        editaccountform = editaccountform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TILIIN
##
@app.route("/accountgroups/editaccount/<account_id>/", methods=["POST"])
@login_required(role="admin")
def accountgroup_edit_account(account_id):

    print("Tehdään tilille jotain")

    editaccountform = AccountForm(request.form)

    print("id:", editaccountform.id.data)
    print("group_id:", editaccountform.accountgroup_id.data)

    if not editaccountform.validate():
        print("Tilin validointi editoidessa ei onnistunut")
        return render_template("accountgroups/list.html",
            action = "EditAccount",
            targetgroup = editaccountform.accountgroup_id.data,
            targetaccount = account_id,
            accountgroups = AccountGroup.findAllGroupsAndAccounts(current_user.get_entity_id()),
            newaccountgroupform = AccountGroupForm(),
            editaccountgroupform = AccountGroupForm(),
            newaccountform = AccountForm())

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        account = Account.query.filter(Account.entity_id == current_user.get_entity_id(), Account.id == account_id).first()
        account.name = editaccountform.name.data
        account.description = editaccountform.description.data
        account.inuse = editaccountform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = Account.query.filter(Account.entity_id == current_user.get_entity_id(), Account.id == account_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("accountgroups_index"))



