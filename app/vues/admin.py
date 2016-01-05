from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os.path as op
from app import app
from app import admin
from app import modeles
from app import db


class VueModele(ModelView):
    '''
    Vue de base qui implémente une authentification
    HTTP. Toutes les autres vues héritent de cette vue.
    '''

    def is_accessible(self):
        auth = request.authorization or request.environ.get(
            'REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('Il faut rentrer les identifiants administrateur.', 401,
                                             {'WWW-Authenticate': 'Basic realm="Identifiants requis"'}
                                             ))
        return True


class VueUtilisateur(VueModele):

    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = False
    can_delete = False

    # Colonnes invisible
    column_exclude_list = ['_mdp']

    # Colonnes pour chercher
    column_searchable_list = ['prenom', 'nom']

    # Colonnes pour filtrer
    column_filters = ['categorie', 'inscription', 'confirmation']


class VueSecteur(VueModele) : 
    
    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = False
    can_delete = False

    # Colonnes pour chercher
    column_searchable_list = ['nom']
    
class VueStation(VueModele) :
        
    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = False
    can_delete = False

    # Colonnes pour chercher
    column_searchable_list = ['nom']
    
    

class VueVehicule(VueModele) :
    
    # Rendre impossible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True

    #Colonnes invisible
    column_exclude_list = ['immatriculation']    
    
    #Colonnes pour chercher
    column_searchable_list = ['marque','couleur']    

class VueConducteur(VueModele) :

    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = False
    can_delete = False    
        
    #Colonnes pour chercher
    column_searchable_list = ['nom','prenom']
    
       

# Utilisateurs
admin.add_view(VueUtilisateur(modeles.Utilisateur, db.session))

# Secteurs
admin.add_view(VueSecteur(modeles.Secteur, db.session))

# Stations
admin.add_view(VueStation(modeles.Station, db.session))

# Vehicules
admin.add_view(VueVehicule(modeles.Vehicule, db.session))

# Conducteurs
admin.add_view(VueConducteur(modeles.Conducteur, db.session))
