from flask import Blueprint, render_template

# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/conducteur')


@conducteurbp.route('/accueil', methods=['GET', 'POST'])
def conducteur_accueil():
    p='Thibault'
    return render_template('conducteur/accueil.html', titre='Conducteur',prenom=p)