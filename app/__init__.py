from flask import Flask

app = Flask(__name__)

# Générer l'application avec les options du fichier config.py
app.config.from_object('config')

# Se connecter à la base de données
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Mettre en place le serveur email
from flask.ext.mail import Mail
mail = Mail(app)

# Mettre en place l'outil pour générer des clés secrètes
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Ajouter une interface administrateur
from flask_admin import Admin
admin = Admin(app, name='Admin', template_mode='bootstrap3')

# Importer les vues
from app.vues import principal, utilisateur, erreur, admin, api, conducteur
app.register_blueprint(utilisateur.utilisateurbp)
app.register_blueprint(api.apibp)
app.register_blueprint(conducteur.conducteurbp)

# Mettre en place la gestion de compte utilisateur
from flask.ext.login import LoginManager
from app.modeles import Utilisateur

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'utilisateurbp.connexion'


@login_manager.user_loader
def load_user(telephone):
    return Utilisateur.query.filter(Utilisateur.telephone == telephone).first()
