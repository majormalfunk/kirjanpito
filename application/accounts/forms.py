from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class AccountForm(FlaskForm):
    id = IntegerField("Tunnus")
    number = IntegerField("Tilin numero", [validators.NumberRange(min=1000, max=9999, message="Tilinumeron pitää olla välillä 1000..9999")])
    name = StringField("Tilin nimi", [validators.Length(min=4, max=100, message="Nimen pituuden pitää olla välillä 4..100")])
    description = StringField("Kuvaus", [validators.Length(min=1, max=255, message="Kuvauksen pituuden pitää olla välillä 1..255")])
    accountgroup_id = IntegerField("Tiliryhm&auml;")
    inuse = BooleanField("K&auml;yt&ouml;ss&auml;")
 
    class Meta:
        csrf = False

