from flask import Blueprint, jsonify
from app import app, db
from app.formulaires import utilisateur as fu
import pandas as pd
import datetime

apibp = Blueprint('apibp', __name__, url_prefix='/api')


def nettoyer(colonne):
    # Convertir les dates au format iso
    if colonne.dtype == 'datetime64[ns]':
        colonne = colonne.apply(lambda x: x.isoformat())
    # Convertir les booléens et NoneType en string
    if colonne.dtype == 'bool':
        colonne = colonne.apply(lambda x: 'True' if x is True else 'False')
    colonne = colonne.apply(lambda x: 'None' if x is None else x)
    return colonne


def to_json(table):
    requete = db.session.execute("SELECT * FROM {}".format(table))
    attributs = requete.keys()
    lignes = requete.fetchall()
    table = pd.DataFrame(lignes, columns=attributs)
    table = table.apply(nettoyer)
    json = table.to_dict(orient='records')
    return json


@apibp.route('/<table>', methods=['GET'])
def api_table(table):
    try:
        json = to_json(table)
        return jsonify({'data': json, 'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
