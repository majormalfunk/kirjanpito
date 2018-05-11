from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.ledgers.models import LedgerDocument
from application.ledgers.forms import LedgerDocumentForm
from application.ledgers.models import LedgerRow
from application.ledgers.forms import LedgerRowForm
from application.documenttypes.models import DocumentType
from application.accounts.models import Account
from application.domains.models import Domain

##
## PERUSREITTI
##
@app.route("/ledgers", methods=["GET", "POST"])
@login_required(role="admin")
def ledgers_index():

    print("*** ledgers_index ***")

    fiscalyear_id = None
    fiscalperiod_id = None
    ledgerdocuments = LedgerDocument.findLedgerDocuments(
        current_user.get_entity_id(), fiscalyear_id, fiscalperiod_id)

    return render_template("ledgers/list.html",
        action = "NoAction",
        targetledger = -1,
        ledgerdocuments = ledgerdocuments)

##
## TÄMÄ REITTI, KUN NÄYTETÄÄN TALLENNETTU TOSITE
##
@app.route("/ledgers/document/<ledgerdocument_id>", methods=["GET", "POST"])
@login_required(role="admin")
def ledgers_document(ledgerdocument_id):

    print("*** ledgers_document ***")

    documenttypes = getDocumentTypes()
    accounts = getAccounts()
    domains = getDomains()

    ledgerdocumentform = getLedgerDocumentInAForm(ledgerdocument_id)

    ledgerrows = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.ledgerdocument_id == ledgerdocument_id).order_by(LedgerRow.id)
    newledgerrowform = newLedgerRowForm(ledgerdocument_id)

    return render_template("ledgers/document.html",
        action = "ShowLedgerDocument",
        ledgerdocumentform = ledgerdocumentform,
        documenttypes = documenttypes,
        accounts = accounts,
        domains = domains,
        targetledgerrow = -1,
        ledgerrows = ledgerrows,
        newledgerrowform = newledgerrowform)

##
## TÄMÄ REITTI, KUN HALUTAAN LISÄTÄ UUSI TOSITE
##
@app.route("/ledgers/recordnew", methods=["POST"])
@login_required(role="admin")
def ledgers_recordnew_document():

    print("*** ledgers_new_document ***")

    documenttypes = getDocumentTypes()

    return render_template("ledgers/document.html",
        action = "NewLedgerDocument",
        ledgerdocumentform = LedgerDocumentForm(),
        documenttypes = documenttypes)

##
## TÄMÄ REITTI, KUN TALLENNETAAN UUSI TOSITE
##
@app.route("/ledgers/savenew", methods=["POST"])
@login_required(role="admin")
def ledgers_savenew_document():

    print("*** ledgers_savenew_document() ***")

    ledgerdocumentform = LedgerDocumentForm(request.form)

    print("Yritetään tallentaa uusi tosite tietokantaan")

    docnum = LedgerDocument.nextDocumentNumber(current_user.get_entity_id(), ledgerdocumentform.documenttype_id.data)

    doc = LedgerDocument(
        ledgerdocumentform.documenttype_id.data,
        docnum,
        ledgerdocumentform.ledgerdate.data,
        ledgerdocumentform.description.data,
        current_user.get_username(),
        None,
        current_user.get_entity_id())

    try:
        db.session().add(doc)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä tositetta tietokantaan")
        pass

    return redirect(url_for("ledgers_index"))
    
##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TOSITTEESEEN
##
@app.route("/ledgers/editdocument/<ledgerdocument_id>/", methods=["POST"])
@login_required(role="admin")
def ledgers_edit_document(ledgerdocument_id):

    print("Tehdään tositteelle " + ledgerdocument_id + " jotain")

    editledgerdocumentform = LedgerDocumentForm(request.form)
    print("ledgerdocument_id on " + str(editledgerdocumentform.id.data))
    
    ledgerrows = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.ledgerdocument_id == ledgerdocument_id).order_by(LedgerRow.id)
    newledgerrowform = newLedgerRowForm(ledgerdocument_id)

    if not editledgerdocumentform.validate():
        documenttypes = getDocumentTypes()
        accounts = getAccounts()
        domains = getDomains()

        return render_template("ledgers/document.html",
        action = "EditLedgerDocument",
        ledgerdocumentform = editledgerdocumentform,
        documenttypes = documenttypes,
        accounts = accounts,
        domains = domains,
        ledgerrows = ledgerrows,
        newledgerrowform = newledgerrowform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        ledgerdocument = LedgerDocument.query.filter(LedgerDocument.entity_id == current_user.get_entity_id(), LedgerDocument.id == ledgerdocument_id).first()
        print("ledgerdocument id : " + str(ledgerdocument.id))
        print("ledgerdocument date : " + str(ledgerdocument.ledgerdate))
        ledgerdocument.ledgerdate = editledgerdocumentform.ledgerdate.data
        ledgerdocument.description = editledgerdocumentform.description.data
        ledgerdocument.recorded_by = current_user.get_username()
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass
        return redirect(url_for("ledgers_document", ledgerdocument_id = ledgerdocument_id))

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = LedgerDocument.query.filter(LedgerDocument.entity_id == current_user.get_entity_id(), LedgerDocument.id == ledgerdocument_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass
        return redirect(url_for("ledgers_index"))


##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TOSITERIVI
##
@app.route("/ledgers/recordledgerrow/<ledgerdocument_id>/", methods=["POST"])
@login_required(role="admin")
def ledgers_record_ledgerrow(ledgerdocument_id):

    print("*** ledgers_record_ledgerrow ***")

    ledgerrowform = LedgerRowForm(request.form)
    ledgerrowform.fixAmounts()
    ledgerrowform.id.data = 0

    if not ledgerrowform.validate():
        print("Validointi ei onnistunut")

        documenttypes = getDocumentTypes()
        accounts = getAccounts()
        domains = getDomains()

        ledgerdocumentform = getLedgerDocumentInAForm(ledgerdocument_id)

        ledgerrows = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.ledgerdocument_id == ledgerdocument_id).order_by(LedgerRow.id)
        newledgerrowform = ledgerrowform

        return render_template("ledgers/document.html",
            action = "FixNewLedgerRow",
            ledgerdocumentform = ledgerdocumentform,
            documenttypes = documenttypes,
            accounts = accounts,
            domains = domains,
            targetledgerrow = -1,
            ledgerrows = ledgerrows,
            fixnewledgerrowform = ledgerrowform)

    print("Yritetään tallentaa tietokantaan")

    ledgerrow = LedgerRow(ledgerdocument_id,
                ledgerrowform.account_id.data,
                (ledgerrowform.debit.data-ledgerrowform.credit.data),
                ledgerrowform.domain_id.data,
                ledgerrowform.description.data,
                current_user.get_username(),
                current_user.get_entity_id())

    try:
        db.session().add(ledgerrow)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä tositeriviä tietokantaan")
        pass

    return redirect(url_for("ledgers_document", ledgerdocument_id = ledgerdocument_id))


##
## TÄMÄ REITTI, KUN HALUTAAN MUOKATA TOSITERIVIÄ
##
@app.route("/ledgers/editledgerrow/<ledgerrow_id>/", methods=["POST"])
@login_required(role="admin")
def ledgers_edit_ledgerrow(ledgerrow_id):

    print("*** ledgers_edit_ledgerrow ***")

    editledgerrowform = LedgerRowForm(request.form)
    ledgerdocument_id = editledgerrowform.ledgerdocument_id.data

    if not editledgerrowform.validate():

        documenttypes = getDocumentTypes()
        accounts = getAccounts()
        domains = getDomains()

        ledgerdocumentform = getLedgerDocumentInAForm(ledgerdocument_id)

        ledgerrows = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.ledgerdocument_id == ledgerdocument_id).order_by(LedgerRow.id)
        newledgerrowform = newLedgerRowForm(ledgerdocument_id)

        return render_template("ledgers/document.html",
            action = "EditLedgerRow",
            targetledgerrow = ledgerrow_id,
            documenttypes = documenttypes,
            accounts = accounts,
            domains = domains,
            ledgerrows = ledgerrows,
            ledgerdocumentform = ledgerdocumentform,
            editledgerrowform = editledgerrowform,
            newledgerrowform = newledgerrowform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        ledgerrow = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.id == ledgerrow_id).first()
        ledgerrow.account_id = editledgerrowform.account_id.data
        editledgerrowform.fixAmounts()
        ledgerrow.amount = (editledgerrowform.debit.data-editledgerrowform.credit.data)
        ledgerrow.domain_id = editledgerrowform.domain_id.data
        ledgerrow.description = editledgerrowform.description.data
        ledgerrow.recorded_by = current_user.get_username()
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.id == ledgerrow_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("ledgers_document", ledgerdocument_id = ledgerdocument_id))




##
## TÄMÄ REITTI, KUN VALITTU TOSITERIVI
##
@app.route("/ledgers/selectledgerrow/<ledgerrow_id>/", methods=["POST"])
@login_required(role="admin")
def ledgers_select_ledgerrow(ledgerrow_id):

    print("*** ledgers_select_ledgerrow ***")

    print("Valittu editoitavaksi tositerivi id = " + ledgerrow_id)

    editledgerrowform = getLedgerRowInAForm(ledgerrow_id)
    ledgerdocument_id = editledgerrowform.ledgerdocument_id.data
    ledgerdocumentform = getLedgerDocumentInAForm(ledgerdocument_id)
    ledgerrows = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.ledgerdocument_id == ledgerdocument_id).order_by(LedgerRow.id)
    newledgerrowform = LedgerRowForm()
    newledgerrowform.ledgerdocument_id.data = ledgerdocument_id
    documenttypes = getDocumentTypes()
    accounts = getAccounts()
    domains = getDomains()


    return render_template("ledgers/document.html",
        action = "EditLedgerRow",
        targetledgerrow = ledgerrow_id,
        documenttypes = documenttypes,
        accounts = accounts,
        domains = domains,
        ledgerrows = ledgerrows,
        ledgerdocumentform = ledgerdocumentform,
        editledgerrowform = editledgerrowform,
        newledgerrowform = newledgerrowform)


def getLedgerDocumentInAForm(ledgerdocument_id):

    ledgerdocument = LedgerDocument.query.filter(LedgerDocument.entity_id == current_user.get_entity_id(), LedgerDocument.id == ledgerdocument_id).first()

    ledgerdocumentform = LedgerDocumentForm()
    ledgerdocumentform.id.data = ledgerdocument.id
    ledgerdocumentform.documenttype_id.data = ledgerdocument.documenttype_id
    ledgerdocumentform.documentnumber.data = ledgerdocument.documentnumber
    ledgerdocumentform.ledgerdate.data = ledgerdocument.ledgerdate
    ledgerdocumentform.description.data = ledgerdocument.description
    ledgerdocumentform.recorded_by.data = ledgerdocument.recorded_by
    ledgerdocumentform.approved_by.data = ledgerdocument.approved_by

    return ledgerdocumentform

def getLedgerRowInAForm(ledgerrow_id):

    ledgerrow = LedgerRow.query.filter(LedgerRow.entity_id == current_user.get_entity_id(), LedgerRow.id == ledgerrow_id).first()

    ledgerrowform = LedgerRowForm()
    ledgerrowform.id.data = ledgerrow.id
    ledgerrowform.account_id.data = ledgerrow.account_id
    if ledgerrow.amount > 0 :
        ledgerrowform.debit.data = ledgerrow.amount
        ledgerrowform.credit.data = 0
    else :
        ledgerrowform.debit.data = 0
        ledgerrowform.credit.data = ledgerrow.amount * (-1)
    ledgerrowform.domain_id.data = ledgerrow.domain_id
    ledgerrowform.description.data = ledgerrow.description
    ledgerrowform.recorded_by.data = ledgerrow.recorded_by
    ledgerrowform.ledgerdocument_id.data = ledgerrow.ledgerdocument_id

    return ledgerrowform

def newLedgerRowForm(ledgerdocument_id):

    newledgerrowform = LedgerRowForm()
    newledgerrowform.ledgerdocument_id.data = ledgerdocument_id
    newledgerrowform.debit.data = int(0)
    newledgerrowform.credit.data = int(0)

    return newledgerrowform

def getDocumentTypes():
    return DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(
        DocumentType.doctype)

def getAccounts():
    return Account.query.filter(Account.entity_id == current_user.get_entity_id()).order_by(
        Account.number)

def getDomains():
    return Domain.query.filter(Domain.entity_id == current_user.get_entity_id()).order_by(
        Domain.code)
