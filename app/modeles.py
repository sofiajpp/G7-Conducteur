from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from geoalchemy2 import Geometry


class Utilisateur(db.Model, UserMixin):

    ''' Un utilisateur du site web. '''

    __tablename__ = 'utilisateurs'

    telephone = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    confirmation = db.Column(db.Boolean)
    categorie = db.Column(db.String)
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    notification_email = db.Column(db.Boolean)
    notification_sms = db.Column(db.Boolean)
    inscription = db.Column(db.DateTime)
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    _mdp = db.Column(db.String)

    @hybrid_property
    def mdp(self):
        return self._mdp

    @mdp.setter
    def _set_password(self, plaintext):
        self._mdp = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return True
        return bcrypt.check_password_hash(self.mdp, plaintext)

    def get_id(self):
        return self.telephone


class Notification(db.Model):

    ''' Une notification envoyée à un utilisateur. '''

    __tablename__ = 'notifications'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    moment = db.Column(db.DateTime)
    sujet = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'course', 'moment',
                                name='pk_notifications'),
    )


class Bannissement(db.Model):

    ''' Un banissement d'un utilisateur. '''

    __tablename__ = 'banissements'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    raison = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'debut',
                                name='pk_bannissements'),
    )


class Habitude(db.Model):

    '''
    Une adresse que l'utilisateur a l'habitude de choisir comme point de
    départ.
    '''

    __tablename__ = 'habitudes'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'adresse', name='pk_habitudes'),
    )


class Conducteur(db.Model):

    ''' Un conducteur de taxi. '''

    __tablename__ = 'conducteurs'

    telephone = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    libre = db.Column(db.Boolean)
    station = db.Column(db.String, db.ForeignKey('stations.nom'))
    position = db.Column(Geometry('POINT'))
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    inscription = db.Column(db.DateTime)


class Penalites(db.Model):

    ''' Une pénalité infligée à un conducteur. '''

    __tablename__ = 'penalites'

    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    raison = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('conducteur', 'debut', name='pk_penalites'),
    )


class Messages(db.Model):

    ''' Un message envoyé à un conducteur. '''

    __tablename__ = 'messages'

    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    moment = db.Column(db.DateTime)
    sujet = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('conducteur', 'moment', name='pk_messages'),
    )


class Positions(db.Model):

    ''' Une position d'un conducteur à un moment donné. '''

    __tablename__ = 'positions'

    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    moment = db.Column(db.DateTime)
    positions = db.Column(Geometry('POINT'))

    __table_args__ = (
        db.PrimaryKeyConstraint('conducteur', 'moment', name='pk_positions'),
    )


class Vehicule(db.Model):

    ''' Une vehicule appartient à un conducteur. '''

    __tablename__ = 'vehicules'

    immatriculation = db.Column(db.String, primary_key=True)
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    places = db.Column(db.Integer, db.CheckConstraint('1 <= places'))
    couleur = db.Column(db.String)
    marque = db.Column(db.String)


class Privilege(db.Model):

    ''' Un lien entre un utilisateur et un conducteur. '''

    __tablename__ = 'privileges'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'conducteur',
                                name='pk_privileges'),
    )


class Adresse(db.Model):

    ''' Un adresse géographique. '''

    __tablename__ = 'adresses'

    identifiant = db.Column(db.Integer, autoincrement=True, primary_key=True)
    adresse = db.Column(db.String)
    numero = db.Column(db.String)
    cp = db.Column(db.Integer)
    ville = db.Column(db.String)
    position = db.Column(Geometry('POINT'))


class Station(db.Model):

    ''' Une station contenant des taxis. '''

    __tablename__ = 'stations'

    nom = db.Column(db.String, primary_key=True)
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    distance = db.Column(db.Float, db.CheckConstraint('0 <= distance'))
    secteur = db.Column(db.String, db.ForeignKey('secteurs.nom'))


class Secteur(db.Model):

    ''' Une secteur contenant des stations. '''

    __tablename__ = 'secteurs'

    nom = db.Column(db.String, primary_key=True)
    surface = db.Column(Geometry('POLYGON'))


class Course(db.Model):

    ''' Une demande de course qui devient une course terminée. '''

    __tablename__ = 'courses'

    numero = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trouvee = db.Column(db.Boolean)
    finie = db.Column(db.Boolean)
    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    places = db.Column(db.Integer, db.CheckConstraint('1 <= places'))
    priorite = db.Column(db.String)
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    retour = db.Column(db.Boolean)
    commentaire = db.Column(db.String)
    bagages = db.Column(db.Boolean)
    animaux = db.Column(db.Boolean)
    gare = db.Column(db.Boolean)
    nombreux = db.Column(db.Boolean)
    depart = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    arrivee = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))

    __table_args__ = (
        db.CheckConstraint('debut < fin', name='debut_inf_fin_check'),
    )


class Etape(db.Model):

    ''' Une étape d'une course. '''

    __tablename__ = 'etapes'

    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    moment = db.Column(db.DateTime)
    position = db.Column(Geometry('POINT'))

    __table_args__ = (
        db.PrimaryKeyConstraint('course', 'moment', name='pk_etapes'),
    )


class Proposition(db.Model):

    ''' Une proposition de course faite à un conducteur. '''

    __tablename__ = 'propositions'

    numero = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    moment = db.Column(db.DateTime)


class Refus(db.Model):

    ''' Un refus explicite ou implicite à une proposition. '''

    __tablename__ = 'refus'

    proposition = db.Column(db.Integer, db.ForeignKey('propositions.numero'))
    moment = db.Column(db.DateTime)
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    explicite = db.Column(db.Boolean)

    __table_args__ = (
        db.PrimaryKeyConstraint('proposition', 'moment', name='pk_refus'),
    )


class Facture(db.Model):

    ''' Une facture relative à une course. '''

    __tablename__ = 'factures'

    course = db.Column(db.Integer, db.ForeignKey('courses.numero'),
                       primary_key=True)
    forfait = db.Column(db.String)
    estimation = db.Column(db.Float, db.CheckConstraint('0 <= estimation'))
    montant = db.Column(db.Float, db.CheckConstraint('0 <= montant'))
    rabais = db.Column(db.Float, db.CheckConstraint(
        '0 <= rabais AND rabais <= 1'))
    paiement = db.Column(db.String)
