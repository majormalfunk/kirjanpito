from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, DecimalField, DateField
from wtforms import validators

class LedgerDocumentForm(FlaskForm):
    id = IntegerField("Tunnus")
    documenttype_id = IntegerField("Tositelaji")
    doctype = StringField("Tositelaji")
    documentnumber = IntegerField("Tositenumero")
    ledgerdate = DateField("Tositepäivä", [validators.DataRequired("Tositepäivä on pakollinen")], format="%d.%m.%Y")
    description = StringField("Kuvaus", [validators.Length(max=255, message="Kuvauksen pituus saa olla enintää 255")])
    recorded_by = StringField("Käsittelijä")
    approved_by = StringField("Hyväksyjä")

    class Meta:
        csrf = False

class LedgerRowForm(FlaskForm):
    id = IntegerField("Tunnus")
    account_id = IntegerField("Tili")
    debet = DecimalField("Debet", places=2, rounding=None, use_locale=True, number_format=None)
    kredit = DecimalField("Debet", places=2, rounding=None, use_locale=True, number_format=None)
    activity_id = IntegerField("Toiminnon tunnus")
    domain_id = IntegerField("Kustannuspaikan tunnus")
    description = StringField("Kuvaus", [validators.Length(max=255, message="Kuvauksen pituus saa olla enintää 255")])
    recorded_by = StringField("Käsittelijä")
    ledgerdocument_id = IntegerField("Tosite")

    class Meta:
        csrf = False
