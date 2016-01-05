# Production

Ce dossier contient l'application finale, celle qui doit marcher sans faille.

## Architecture

Blablabla.

## Utilisation

Il faut d'abord s'assurer que les valeurs dans ``config.py`` soient cohérentes, c'est à dire bien faire en sorte que le port et le mot de passe de PostgreSQL soient les mêmes que ceux de l'ordinateur d'où l'application est lancée. Si la base de données a déjà été créée elle peut être supprimée en lancant le script ``suppression.py``.

```sh
# Installer les librairies
pip install -r requirements.txt
# Créer la base de données
python creation.py
# Lancer le site web
python run.py
```

Ensuite il suffit de consulter l'URL ``localhost:5000`` dans le navigateur.

## Heroku

Se référer au dossier ``setup/``.
