from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)
from app.modeles import Utilisateur


class Demande(Form):

    ''' Demande de réservation d'un taxi par un utilisateur. '''

    ville_dep = TextField(description='Ville de départ')
    cp_dep = TextField(description='Code postal', validators=[Length(max=5)])
    adresse_dep = TextField(description='Adresse')
    numero_dep = TextField(description='Numéro')

    ville_arr = TextField(description="Ville d'arrivée")
    cp_arr = TextField(description='Code postal', validators=[Length(max=5)])
    adresse_arr = TextField(description='Adresse')
    numero_arr = TextField(description='Numéro')
