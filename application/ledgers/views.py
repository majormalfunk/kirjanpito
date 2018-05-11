from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.ledgers.models import LedgerDocument
from application.ledgers.forms import LedgerDocumentForm
from application.documenttypes.models import DocumentType

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
        ##LedgerDocument.query.filter(LedgerDocument.entity_id == current_user.get_entity_id()).order_by(
        ##    LedgerDocument.ledgerdate, LedgerDocument.documenttype_id, LedgerDocument.documentnumber),
        ##documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(
        ##DocumentType.doctype)

##
## TÄMÄ REITTI, KUN NÄYTETÄÄN TALLENNETTU TOSITE
##
@app.route("/ledgers/document/<ledgerdocument_id>", methods=["GET", "POST"])
@login_required(role="admin")
def ledgers_document(ledgerdocument_id):

    print("*** ledgers_document ***")

    documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(
        DocumentType.doctype)

    ledgerdocument = LedgerDocument.query.filter(LedgerDocument.entity_id == current_user.get_entity_id(), LedgerDocument.id == ledgerdocument_id).first()


    print("Valittu tosite id " + str(ledgerdocument_id) + "(kannasta " + str(ledgerdocument.id) + ")")

    ledgerdocumentform = LedgerDocumentForm()
    ledgerdocumentform.id.data = ledgerdocument.id
    ledgerdocumentform.documenttype_id.data = ledgerdocument.documenttype_id
    ledgerdocumentform.documentnumber.data = ledgerdocument.documentnumber
    ledgerdocumentform.ledgerdate.data = ledgerdocument.ledgerdate
    ledgerdocumentform.description.data = ledgerdocument.description
    ledgerdocumentform.recorded_by.data = ledgerdocument.recorded_by
    ledgerdocumentform.approved_by.data = ledgerdocument.approved_by

    return render_template("ledgers/document.html",
        action = "ShowLedgerDocument",
        ledgerdocumentform = ledgerdocumentform,
        documenttypes = documenttypes)

##
## TÄMÄ REITTI, KUN HALUTAAN LISÄTÄ UUSI TOSITE
##
@app.route("/ledgers/recordnew", methods=["POST"])
@login_required(role="admin")
def ledgers_recordnew_document():

    print("*** ledgers_new_document ***")

    documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(
        DocumentType.doctype)

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

    print("TOIMIIKO? " + str(docnum))
    doc = LedgerDocument(
        ledgerdocumentform.documenttype_id.data,
        docnum,
        ledgerdocumentform.ledgerdate.data,
        ledgerdocumentform.description.data,
        current_user.get_username(),
        None,
        current_user.get_entity_id())

    ##try:
    db.session().add(doc)
    db.session().commit()
    ##  print("Tallennus onnistui")
    ##except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
    ##    print("Tapahtui virhe lisättäessä tositetta tietokantaan")
    ##    pass

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
    ##editledgerdocumentform.id.data = ledgerdocument_id

    if not editledgerdocumentform.validate():
        documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(
            DocumentType.doctype)

        return render_template("ledgers/document.html",
        action = "EditLedgerDocument",
        ledgerdocumentform = editledgerdocumentform,
        documenttypes = documenttypes)

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


