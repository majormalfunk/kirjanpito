from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.domains.models import Domain
from application.domains.forms import DomainForm

##
## PERUSREITTI
##
@app.route("/domains", methods=["GET", "POST"])
@login_required(role="admin")
def domains_index():

    print("*** domains_index ***")

    return render_template("domains/list.html",
    action = "NoAction",
    targetdomain = -1,
    domains = Domain.query.filter(Domain.entity_id == current_user.get_entity_id()).order_by(Domain.orderer),
    newdomainform = DomainForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI KUSTANNUSPAIKKA
##
@app.route("/domains/newdomain/", methods=["POST"])
@login_required(role="admin")
def domain_new_domain():

    domainform = DomainForm(request.form)

    if not domainform.validate():
        print("Validointi ei onnistunut")
        return render_template("domains/list.html",
            action = "FixNewDomain",
            targetdomain = -1,
            domains = Domain.query.filter(Domain.entity_id == current_user.get_entity_id()).order_by(Domain.orderer),
            fixnewdomainform = domainform,
            newdomainform = DomainForm())

    print("Yritetään tallentaa tietokantaan")

    domain = Domain(domainform.orderer.data,
                domainform.code.data,
                domainform.name.data,
                domainform.description.data,
                domainform.inuse.data,
                current_user.get_entity_id())
    try:
        db.session().add(domain)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä kustannuspaikkaa tietokantaan")
        pass

    return redirect(url_for("domains_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU KUSTANNUSPAIKKA EDITOITAVAKSI
##
@app.route("/domains/selectdomain/<domain_id>/", methods=["POST"])
@login_required(role="admin")
def domain_select_domain(domain_id):

    print("Valittu editoitavaksi kustannuspaikka id = " + domain_id)

    editdomainform = DomainForm(request.form)
    domain = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
    editdomainform.id.data = domain.id
    editdomainform.orderer.data = domain.orderer
    editdomainform.code.data = domain.code
    editdomainform.name.data = domain.name
    editdomainform.description.data = domain.description
    editdomainform.inuse.data = domain.inuse

    return render_template("domains/list.html",
        action = "EditDomain",
        targetdomain = domain_id,
        domains = Domain.query.filter(Domain.entity_id == current_user.get_entity_id()).order_by(Domain.orderer),
        newdomainform = DomainForm(),
        editdomainform = editdomainform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA KUSTANNUSPAIKKAAN
##
@app.route("/domains/editdomain/<domain_id>/", methods=["POST"])
@login_required(role="admin")
def domain_edit_domain(domain_id):

    print("Tehdään kustannuspaikalle " + domain_id + " jotain")

    editdomainform = DomainForm(request.form)
    print("domainid on " + str(editdomainform.id.data))
    editdomainform.id.data = domain_id

    if not editdomainform.validate():
        return render_template("domains/list.html",
            action = "EditDomain",
            targetdomain = domain_id,
            domains = Domain.query.filter(Domain.entity_id == current_user.get_entity_id()).order_by(Domain.orderer),
            newdomainform = DomainForm(),
            editdomainform = editdomainform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        domain = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
        domain.orderer = editdomainform.orderer.data
        domain.name = editdomainform.name.data
        domain.description = editdomainform.description.data
        domain.inuse = editdomainform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = Domain.query.filter(Domain.entity_id == current_user.get_entity_id(), Domain.id == domain_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("domains_index"))

