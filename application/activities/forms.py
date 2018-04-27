from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms import validators

class ActivityForm(FlaskForm):
    id = IntegerField("Tunnus")
    orderer = IntegerField("Järjestysnumero", [validators.NumberRange(min=1, message="Pitää olla suurempi kuin 1")])
    code = StringField("Toiminto", [validators.Length(min=1, max=10, message="Pituus pitää olla 1..10")])
    name = StringField("Toiminnon nimi", [validators.Length(min=4, max=100, message="Pituus pitää olla 4..100")])
    description = StringField("Kuvaus", [validators.Length(max=255, message="Pituus saa olla enintään 255")])
    inuse = BooleanField("Käytössä")
 
    class Meta:
        csrf = False

