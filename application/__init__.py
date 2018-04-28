# Tuodaan Flask käyttöön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    # Käytetään HEROKUssa PostgreSQL:ää
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    # Ja paikallisissa testeissä SQLiteä
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounting.db"

# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

# Kirjautuminen
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

# Tallennettavan salasanan hashaaminen
import passlib

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Sinun pitää kirjautua voidaksesi käyttää toiminnallisuutta"

# roles in login_required
from functools import wraps

def login_required(role="any"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "any":
                unauthorized = True
                
                if current_user.role == role:
                    unauthorized = False

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Luetaan kansiosta application/ tiedostojen sisältö
from application import views

# Ja kansion application/accountgroups/ tiedostojen sisältö
from application.accountgroups import models
from application.accountgroups import views
# Ja kansion application/accounts/ tiedostojen sisältö
from application.accounts import models
# Ja kansion application/domains/ tiedostojen sisältö
from application.domains import models
from application.domains import views
# Ja kansion application/activities/ tiedostojen sisältö
from application.activities import models
from application.activities import views
# Ja kansion application/fiscalperiods/ tiedostojen sisältö
from application.fiscalperiods import models
from application.fiscalperiods import views
# Ja kansion application/entity/ tiedostojen sisältö
from application.entity import models
from application.entity import views

from application.auth import models
from application.auth import views
from application.auth.models import UserAccount


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass

