from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class DocumentTypeForm(FlaskForm):
    id = IntegerField("Tunnus")
    doctype = StringField("Tositelaji", [validators.Length(min=1, max=2, message="Pituus pitää olla 1..2")])
    name = StringField("Tositelajin nimi", [validators.Length(min=4, max=100, message="Pituus pitää olla 4..100")])
    description = StringField("Kuvaus", [validators.Length(max=255, message="Pituus saa olla enintään 255")])
    inuse = BooleanField("Käytössä")
 
    class Meta:
        csrf = False

