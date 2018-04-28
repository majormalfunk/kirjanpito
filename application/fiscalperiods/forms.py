from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, DateField
from wtforms import validators

class FiscalYearForm(FlaskForm):
    id = IntegerField("Tunnus")
    name = StringField("Tilikauden nimi", [validators.Length(min=4, max=4, message="Pituus oltava 4")])
    startdate = DateField("Alkupäivä", [validators.DataRequired("Alkupäivä on pakollinen")], format="%d.%m.%Y")
    enddate = DateField("Loppupäivä", [validators.DataRequired("Loppupäivä on pakollinen")], format="%d.%m.%Y")
    closed = BooleanField("Suljettu")
    locked = BooleanField("Lukittu")
 
    class Meta:
        csrf = False

class FiscalPeriodForm(FlaskForm):
    id = IntegerField("Tunnus")
    name = StringField("Jakson nimi", [validators.Length(min=6, max=6, message="Pituus oltava 6")])
    startdate = DateField("Alkupäivä", [validators.DataRequired("Alkupäivä on pakollinen")], format="%d.%m.%Y")
    enddate = DateField("Loppupäivä", [validators.DataRequired("Loppupäivä on pakollinen")], format="%d.%m.%Y")
    closed = BooleanField("Suljettu")
    locked = BooleanField("Lukittu")
    fiscalyear_id = IntegerField("Tilikausi")
 
    class Meta:
        csrf = False

