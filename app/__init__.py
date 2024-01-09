import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

db_context = SQLAlchemy()
#DB_NAME = os.environ['DATABASE_NAME']

def create_app() -> Flask:
    app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    db_context.init_app(app)
    migrate = Migrate(app, db_context)

    __register_blueprint(app)
    __register_login_manager(app)
    
    return app

def __register_blueprint(app:Flask):
    from .website.controllers.client.dashboard_controller import dashboard
    from .website.controllers.auth_controller import auth
    from .website.controllers.admin.book_controller import admin_book
    from .website.controllers.admin.user_controller import admin_user
    from .website.controllers.admin.dashboard_controller import admin_dashboard

    app.register_blueprint(dashboard, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/auth/')
    app.register_blueprint(admin_dashboard, url_prefix='/admin/')
    app.register_blueprint(admin_book, url_prefix = '/admin/book/' )
    app.register_blueprint(admin_user, url_prefix = '/admin/user/' )

def __register_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .website.models.user import User
    with app.app_context():
        db_context.create_all()
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))