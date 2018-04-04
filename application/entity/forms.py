from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class EntityForm(FlaskForm):
    code = StringField("Y-tunnus", [validators.Length(max=9, message="Pituus 0..9")])
    name = StringField("Yhteisön nimi", [validators.Length(min=4, max=100, message="Pituus 4..100")])
    description = StringField("Kuvaus", [validators.Length(min=1, max=255, message="Pituus 1..255")])
 
    class Meta:
        csrf = False

class EntityEditForm(FlaskForm):
    code = StringField("Y-tunnus", [validators.Length(max=9, message="Pituus 0..9")])
    name = StringField("Yhteisön nimi", [validators.Length(min=4, max=100, message="Pituus 4..100")])
    description = StringField("Kuvaus", [validators.Length(min=1, max=255, message="Pituus 1..255")])
 
    class Meta:
        csrf = False
