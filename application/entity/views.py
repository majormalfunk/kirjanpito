from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.entity.models import Entity
from application.entity.forms import EntityForm, EntityEditForm

@app.route("/entity", methods=["GET"])
@login_required(role="admin")
def entity_index():

    print("Userin entity_id on " + str(current_user.get_entity_id()))
    return render_template("entity/edit.html", entity = Entity.query.get(current_user.get_entity_id()))

@app.route("/entity/new/")
@login_required(role="admin")
def entity_form():
    return render_template("entity/new.html", form = EntityForm())

@app.route("/entity/select/", methods=["GET","POST"])
@login_required(role="admin")
def entity_select_for_edit():

    print("Valittu editoitavaksi " + str(current_user.get_entity_id()))

    form = EntityEditForm()
    entity = Entity.query.get(current_user.get_entity_id())
    form.code.data = entity.code
    form.name.data = entity.name
    form.description.data = entity.description

    return render_template("entity/edit.html", form = form)

@app.route("/entity/edit/", methods=["POST"])
@login_required(role="admin")
def entity_edit():

    print("Yritetään tallentaa")

    form = EntityEditForm(request.form)

    if not form.validate():
        return render_template("entity/edit.html", form = form)

    entity = Entity.query.get(current_user.get_entity_id())
    entity.code = form.code.data
    entity.name = form.name.data
    entity.description = form.description.data
    db.session().commit()

    return redirect(url_for("entity_select_for_edit"))

@app.route("/entity/", methods=["POST"])
@login_required(role="admin")
def entity_create():
    form = EntityForm(request.form)

    if not form.validate():
        return render_template("entity/new.html", form = form)

    e = Entity(code=form.code.data, name=form.name.data, description=form.description.data)
    db.session().add(e)
    db.session().commit()

    return redirect(url_for("entity_index"))
