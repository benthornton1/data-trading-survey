import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
    SECRET_KEY = os.environ.get('FLASK_PROJECT_SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True
    UPLOAD_FOLDER='app/static'
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
    MAIL_SERVER=os.environ.get('FLASK_PROJECT_MAIL_SERVER')
    MAIL_PORT=os.environ.get('FLASK_PROJECT_MAIL_PORT')
    MAIL_USE_TLS=os.environ.get('FLASK_PROJECT_MAIL_USE_TLS') is not None
    MAIL_USERNAME=os.environ.get('FLASK_PROJECT_MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('FLASK_PROJECT_MAIL_PASSWORD')
    ADMIN_EMAILS=[os.environ.get('ADMIN_EMAIL')]
    
class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_PROJECT_PRODUCTION_DATABASE')
    MAIL_SUPPRESS_SEND=False
    DEBUG = False
    
class DevelopmentConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG = True

class TestConfig(DefaultConfig):
    USE_RELOADER = False
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'