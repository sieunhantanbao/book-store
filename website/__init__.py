import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
DB_NAME = os.environ['DATABASE_NAME']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    db.init_app(app)

    from .views.dashboard import dashboard
    from .views.auth import auth
    from .views.admin.product_management import admin_product
    from .views.admin.dashboard import admin_dashboard

    app.register_blueprint(dashboard, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/auth/')
    app.register_blueprint(admin_dashboard, url_prefix='/admin/')
    app.register_blueprint(admin_product, url_prefix = '/admin/product/' )


    from .models.db_models import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Db created!')