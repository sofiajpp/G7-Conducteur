from flask import Blueprint, render_template

# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/G7')


@conducteurbp.route('/accueil', methods=['GET', 'POST'])
def conducteur_accueil():
    p='Thibault'
    return render_template('G7.html', titre='G7',prenom=p)