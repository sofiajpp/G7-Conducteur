from app import db
from app import app
from app import modeles
from sqlalchemy import create_engine
import contextlib
import sqlalchemy.exc

uri = app.config['SQLALCHEMY_DATABASE_URI'].split('/')
url = '/'.join(uri[:-1])
bd = uri[-1]

with contextlib.suppress(sqlalchemy.exc.ProgrammingError):
    with create_engine(url,
                       isolation_level='AUTOCOMMIT').connect() as connexion:
        connexion.execute("CREATE DATABASE {} WITH encoding='utf-8'".format(bd))

print('Base de données créée.')

db.session.execute("SET client_encoding='utf-8'")
db.session.execute('CREATE EXTENSION postgis')
db.session.commit()
db.create_all()

print('Tables créées.')