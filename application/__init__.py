# Tuodaan Flask käyttöön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy
# Käytetään accounting.db-nimistä SQLite-tietokantaa. Kolme vinoviivaa
# kertoo, tiedosto sijaitsee tämän sovelluksen tiedostojen kanssa
# samassa paikassa
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounting.db"
# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

# Luetaan kansiosta application/ tiedostojen sisältö
from application import views

# Ja kansion application/accounts/ tiedostojen sisältö
from application.accounts import models
from application.accounts import views

# Kirjautuminen
from application.auth import models
from application.auth import views
from application.auth.models import UserAccount
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Sinun pitää kirjautua voidaksesi käyttää toiminnallisuutta"

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
db.create_all()
