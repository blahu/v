import os

DEBUG = True
## WTForms
WTF_CSRF_ENABLED = True
SECRET_KEY = 'djkdhfdskfhpiuhdfkjdsnfb23i3ug29hen'

## db
SQLALCHEMY_DATABASE_URI = 'postgresql:///{}'.format(os.environ.get('DBURI'))


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# pagination
ITEMS_PER_PAGE = 20
