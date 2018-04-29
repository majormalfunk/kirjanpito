from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.documenttypes.models import DocumentType
from application.documenttypes.forms import DocumentTypeForm

##
## PERUSREITTI
##
@app.route("/documenttypes", methods=["GET", "POST"])
@login_required(role="admin")
def documenttypes_index():

    print("*** documenttypes_index ***")

    return render_template("documenttypes/list.html",
    action = "NoAction",
    targetdocumenttype = -1,
    documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(DocumentType.doctype),
    newdocumenttypeform = DocumentTypeForm())

##
## TÄMÄ REITTI, KUN LISÄTÄÄN UUSI TOSITELAJI
##
@app.route("/documenttypes/newdocumenttype/", methods=["POST"])
@login_required(role="admin")
def documenttype_new_documenttype():

    documenttypeform = DocumentTypeForm(request.form)

    if not documenttypeform.validate():
        print("Validointi ei onnistunut")
        return render_template("documenttypes/list.html",
            action = "FixNewDocumentType",
            targetdocumenttype = -1,
            documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(DocumentType.doctype),
            fixnewdocumenttypeform = documenttypeform,
            newdocumenttypeform = DocumentTypeForm())

    print("Yritetään tallentaa tietokantaan")

    documenttype = DocumentType(documenttypeform.doctype.data,
                documenttypeform.name.data,
                documenttypeform.description.data,
                documenttypeform.inuse.data,
                current_user.get_entity_id())
    try:
        db.session().add(documenttype)
        db.session().commit()
        print("Tallennus onnistui")
    except:
        ## TÄHÄN VIRHETILANTEEN KÄSITTELY
        print("Tapahtui virhe lisättäessä tositelajia tietokantaan")
        pass

    return redirect(url_for("documenttypes_index"))

##
## TÄMÄ REITTI, KUN ON VALITTU TOSITELAJI EDITOITAVAKSI
##
@app.route("/documenttypes/selectdocumenttype/<documenttype_id>/", methods=["POST"])
@login_required(role="admin")
def documenttype_select_documenttype(documenttype_id):

    print("Valittu editoitavaksi tositelaji id = " + documenttype_id)

    editdocumenttypeform = DocumentTypeForm(request.form)
    documenttype = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id(), DocumentType.id == documenttype_id).first()
    editdocumenttypeform.id.data = documenttype.id
    editdocumenttypeform.doctype.data = documenttype.doctype
    editdocumenttypeform.name.data = documenttype.name
    editdocumenttypeform.description.data = documenttype.description
    editdocumenttypeform.inuse.data = documenttype.inuse

    return render_template("documenttypes/list.html",
        action = "EditDocumentType",
        targetdocumenttype = documenttype_id,
        documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(DocumentType.doctype),
        newdocumenttypeform = DocumentTypeForm(),
        editdocumenttypeform = editdocumenttypeform)

##
## TÄMÄ REITTI, KUN OLLAAN TALLENTAMASSA MUUTOSTA TOSITELAJIIN
##
@app.route("/documenttypes/editdocumenttype/<documenttype_id>/", methods=["POST"])
@login_required(role="admin")
def documenttype_edit_documenttype(documenttype_id):

    print("Tehdään tositelajille " + documenttype_id + " jotain")

    editdocumenttypeform = DocumentTypeForm(request.form)
    print("documenttypeid on " + str(editdocumenttypeform.id.data))
    editdocumenttypeform.id.data = documenttype_id

    if not editdocumenttypeform.validate():
        return render_template("documenttypes/list.html",
            action = "EditDocumentType",
            targetdocumenttype = documenttype_id,
            documenttypes = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id()).order_by(DocumentType.doctype),
            newdocumenttypeform = DocumentTypeForm(),
            editdocumenttypeform = editdocumenttypeform)

    if "action_update" in request.form:
        print("Yritetään tallentaa")
        documenttype = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id(), DocumentType.id == documenttype_id).first()
        documenttype.name = editdocumenttypeform.name.data
        documenttype.description = editdocumenttypeform.description.data
        documenttype.inuse = editdocumenttypeform.inuse.data
        try:
            db.session().commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    elif "action_delete" in request.form:
        print("Yritetään poistaa")
        obsolete = DocumentType.query.filter(DocumentType.entity_id == current_user.get_entity_id(), DocumentType.id == documenttype_id).first()
        try:
            db.session().delete(obsolete)
            db.session.commit()
        except:
            ## TÄHÄN VIRHETILANTEEN KÄSITTELY
            pass

    return redirect(url_for("documenttypes_index"))

