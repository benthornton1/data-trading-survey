import os
import atexit

from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import ProductionConfig, DevelopmentConfig, TestConfig 

bp = Blueprint('base', __name__)

from app import routes

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
scheduler = APScheduler()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()

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
    mail.init_app(app)
    
    from app.scheduler_tasks.check_studies import check_studies
    
    if os.environ['FLASK_ENV'] != 'test':
        scheduler.api_enabled = True
        scheduler.init_app(app)
        scheduler.add_job(id='check_studies_job',trigger='cron',func=check_studies, hour='*', minute=5 ,args=[app])
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown(wait=False))
    
    csrf.init_app(app)
    jwt.init_app(app)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    app.register_blueprint(bp, url_prefix='/')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.study import bp as study_bp
    app.register_blueprint(study_bp, url_prefix='/study')

    from app.responses import bp as responses_bp
    app.register_blueprint(responses_bp, url_prefix='/responses')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
