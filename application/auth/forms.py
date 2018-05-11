from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, IntegerField
from wtforms import validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjätunnus", [
        validators.Length(min=8, max=20, message="Käyttäjätunnuksen pituus pitää olla 8..20")])
    password = PasswordField("Salasana", [
        validators.Required(),
        validators.Length(min=8, max=20, message="Salasanan pituus pitää olla 8..20")])
    confirm = PasswordField("Salasana uudestaan", [
        validators.EqualTo("password", message="Salasanan pitää täsmätä")])
    name = StringField("Nimi", [
        validators.Length(min=4, max=100, message="Nimen pituuden pitää olla 4..100")])
  
    class Meta:
        csrf = False

class UserAccountForm(FlaskForm):
    id = IntegerField("Tunnus")
    username = StringField("Käyttäjätunnus", [
        validators.Length(min=8, max=20, message="Käyttäjätunnuksen pituus pitää olla 8..20")])
    password = PasswordField("Salasana", [
        validators.Required(),
        validators.Length(min=8, max=20, message="Salasanan pituus pitää olla 8..20")])
    confirm = PasswordField("Salasana uudestaan", [
        validators.EqualTo("password", message="Salasanan pitää täsmätä")])
    name = StringField("Nimi", [
        validators.Length(min=4, max=100, message="Nimen pituuden pitää olla 4..100")])
    role = SelectField("Rooli",
        choices=[("admin", "Pääkäyttäjä"), ("approver", "Hyväksyjä"), ("readonly", "Lukuoikeus")]
    )
    class Meta:
        csrf = False

class EditUserAccountForm(FlaskForm):
    id = IntegerField("Tunnus")
    username = StringField("Käyttäjätunnus", [
        validators.Length(min=8, max=20, message="Käyttäjätunnuksen pituus pitää olla 8..20")])
    name = StringField("Nimi", [
        validators.Length(min=4, max=100, message="Nimen pituuden pitää olla 4..100")])
    role = SelectField("Rooli",
        choices=[("admin", "Pääkäyttäjä"), ("approver", "Hyväksyjä"), ("readonly", "Lukuoikeus")]
    )
    class Meta:
        csrf = False
