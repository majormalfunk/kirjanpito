from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class AccountGroupForm(FlaskForm):
    id = IntegerField("Tunnus")
    number = IntegerField("Tiliryhm&auml;n numero", [validators.NumberRange(min=1, max=999, message="Tiliryhmän numero pitää olla välillä 1..999")])
    name = StringField("Tiliryhm&auml;n nimi", [validators.Length(min=4, max=100, message="Nimen pituus pitää olla välillä 4..100")])
    description = StringField("Kuvaus", [validators.Length(max=255, message="Kuvauksen pituus saa olla enintää 255")])
    inuse = BooleanField("K&auml;yt&ouml;ss&auml;")
 
    class Meta:
        csrf = False

