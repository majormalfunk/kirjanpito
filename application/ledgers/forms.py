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
    debit = IntegerField("Debet", [validators.NumberRange(min=0, message="Debet ei saa olla negatiivinen")])
    credit = IntegerField("Kredit", [validators.NumberRange(min=0, message="Kredit ei saa olla negatiivinen")])
    domain_id = IntegerField("Kustannuspaikan tunnus")
    description = StringField("Kuvaus", [validators.Length(max=255, message="Kuvauksen pituus saa olla enintää 255")])
    recorded_by = StringField("Käsittelijä")
    ledgerdocument_id = IntegerField("Tosite")

    def fixAmounts(self):
        print("Fixing amounts!")
        if self.debit.data == None:
            self.debit.data = int(0)
        if self.credit.data == None:
            self.credit.data = int(0)

    class Meta:
        csrf = False
