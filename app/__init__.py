from flask import Flask
from config import ProductionConfig, DevelopmentConfig, TestConfig 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler
import atexit
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os

from flask import Blueprint

bp = Blueprint('base', __name__)

from app import routes


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
scheduler = APScheduler()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    config = None
    if os.environ['FLASK_ENV'] == 'production':
        config = ProductionConfig()
    elif os.environ['FLASK_ENV'] == 'development':
        config = DevelopmentConfig()
        print('THIS APP IS IN DEV CONFIGURATION. DO NOT USE IN PRODUCTION.')
    elif os.environ['FLASK_ENV'] == 'test':
        config = TestConfig()
        print('THIS APP IS IN TEST CONFIGURATION. DO NOT USE IN PRODUCTION.')
    elif config == None:
        print('NO CONFIGURATION SET.')
        
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.scheduler_tasks.check_studies import check_studies
    
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.add_job(id='check_studies_job',trigger='cron',func=check_studies, hour='*', minute=5 ,args=[app])
    scheduler.start()
    
    mail.init_app(app)
    csrf.init_app(app)
    
    app.register_blueprint(bp, url_prefix='/')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.study import bp as study_bp
    app.register_blueprint(study_bp, url_prefix='/study')

    from app.responses import bp as responses_bp
    app.register_blueprint(responses_bp, url_prefix='/responses')
    
    atexit.register(lambda: scheduler.shutdown())

    return app