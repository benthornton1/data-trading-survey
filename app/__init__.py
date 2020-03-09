from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# app=Flask(__name__)
# app.config.from_object(Config)
# db=SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
# mail = Mail(app)
# csrf = CSRFProtect(app)



# from app import routes, models

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
scheduler = APScheduler()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # scheduler.api_enabled = True
    # scheduler.init_app(app)
    # scheduler.start()

    mail.init_app(app)
    csrf.init_app(app)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.study import bp as study_bp
    app.register_blueprint(study_bp, url_prefix='/study')

    from app.responses import bp as responses_bp
    app.register_blueprint(responses_bp, url_prefix='/responses')
    
    return app