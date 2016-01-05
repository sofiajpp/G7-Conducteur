from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)
from app.modeles import Utilisateur


class Unique(object):

    '''
    Validateur fait maison pour s'assurer qu'un
    attribut est unique. Par exemple on ne veut
    pas qu'un utilisateur puisse utiliser une
    adresse email qui a déjà été utilisé pour
    un autre compte. Cette classe suppose qu'on
    utilise SQLAlchemy.
    '''

    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class Oubli(Form):

    ''' Oubli de mot de passe. '''

    email = TextField(validators=[Required(), Email()],
                      description='Adresse email')


class Reinitialisation(Form):

    ''' Reinitisation de mot de passe. '''

    mdp = PasswordField(validators=[
        Required(), Length(min=6),
        EqualTo(
            'confirmation', message='Les mots de passe doivent être ' +
                                    'identiques.')
    ], description='Nouveau mot de passe')
    confirmation = PasswordField(
        description='Confirmer le nouveau mot de passe')


class Connexion(Form):

    ''' Connexion. '''

    email = TextField(validators=[Required(), Email()],
                      description='Adresse email')
    mdp = PasswordField(validators=[Required()],
                        description='Mot de passe')


class Enregistrement(Form):

    ''' Enregistrement. '''

    prenom = TextField(
        validators=[Required(), Length(min=2)], description='Prénom')
    nom = TextField(validators=[Required(), Length(min=2)], description='Nom')
    telephone = TextField(validators=[Required(), Length(min=6),
                                      Unique(Utilisateur, Utilisateur.telephone, 'Ce numéro de téléphone est déjà lié à un compte.')],
                          description='Numéro de téléphone')
    email = TextField(validators=[Required(), Email(),
                                  Unique(Utilisateur, Utilisateur.email, 'Cette adresse email est déjà liée à un compte.')],
                      description='Adresse email')

    ville = TextField(description='Ville')
    cp = TextField(description='Code postal', validators=[Length(max=5)])
    adresse = TextField(description='Adresse')
    numero = TextField(description='Numéro')

    mdp = PasswordField(validators=[
        Required(), Length(min=6),
        EqualTo('confirmation', message='Les mots de passe doivent être identiques.')
    ], description='Mot de passe')
    confirmation = PasswordField(description='Confirmer le mot de passe')


class Modification(Form):

    ''' Edition des données de l'utilisateur. '''

    prenom = TextField(validators=[Required(), Length(min=2)],
                       description='Prénom')
    nom = TextField(validators=[Required(), Length(min=2)],
                    description='Nom')
    telephone = TextField(validators=[Required(), Length(min=6)],
                          description='Numéro de téléphone')
