from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms import validators
  
class LoginForm(FlaskForm):
    username = StringField("K&auml;tt&auml;j&auml;tunnus")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("K&auml;ytt&auml;j&auml;tunnus", [
        validators.Length(min=8, max=20, message="Pituus 8..20")])
    password = PasswordField("Salasana", [
        validators.Required(),
        validators.Length(min=8, max=20, message="Pituus 8..20")])
    confirm = PasswordField("Salasana uudestaan", [
        validators.EqualTo("password", message="Salasanan pit&auml;&auml t&auml;sm&auml;t&auml;")])
    name = StringField("Nimi", [
        validators.Length(min=4, max=100, message="Pituus 4..100")])
  
    class Meta:
        csrf = False