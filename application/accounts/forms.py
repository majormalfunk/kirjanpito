from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class AccountForm(FlaskForm):
    code = IntegerField("Tilin numero", [validators.NumberRange(min=1000, max=9999, message="Sallittu 1000..9999")])
    name = StringField("Tilin nimi", [validators.Length(min=4, max=100, message="Pituus 4..100")])
    description = StringField("Kuvaus", [validators.Length(min=1, max=255, message="Pituus 1..255")])
    inuse = BooleanField("K&auml;yt&ouml;ss&auml;")
 
    class Meta:
        csrf = False

class AccountEditForm(FlaskForm):
    ##code = IntegerField("Tilin numero", [validators.NumberRange(min=1000, max=9999, message="Sallittu 1000..9999")])
    name = StringField("Tilin nimi", [validators.Length(min=4, max=100, message="Pituus 4..100")])
    description = StringField("Kuvaus", [validators.Length(min=1, max=255, message="Pituus 1..255")])
    inuse = BooleanField("K&auml;yt&ouml;ss&auml;")
 
    class Meta:
        csrf = False
