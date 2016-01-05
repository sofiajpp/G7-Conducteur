import json
from app.outils import utile


@utile.MWT(timeout=60 * 60 * 24)
def geocoder(adresse):
    '''
    Geocoder une adresse en (latitude, longitude) grâce à
    l'API de Nominatim.
    '''
    base = 'http://nominatim.openstreetmap.org/search?' \
           'format=json&polygon_geojson=1&q='
    texte = utile.nettoyer(adresse)
    mots_cles = '+'.join(texte.split())
    url = ''.join((base, mots_cles))
    reponse = utile.requete_http(url)
    adresse = json.loads(reponse)[0]
    latitude = float(adresse['lat'])
    longitude = float(adresse['lon'])
    return {
        'lat': latitude,
        'lon': longitude
    }
