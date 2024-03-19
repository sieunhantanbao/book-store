import os
from uuid import UUID
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
import redis

from .database import get_db_context
from .settings import SQLALCHEMY_DATABASE_URL

# Load environment variables from .env file
load_dotenv()

# Caching with Redis
redis_client = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0)

def __page_not_found(e):
    return render_template('common/404.html'), 404


def create_app() -> Flask:
    app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
    
    app.register_error_handler(404, __page_not_found)
    
    __register_blueprint(app)
    __register_login_manager(app)
    
    return app

def __register_blueprint(app:Flask):
    from .website.controllers.client.dashboard_controller import dashboard
    from .website.controllers.client.book_controller import book
    from .website.controllers.auth_controller import auth
    from .website.controllers.admin.category_controller import admin_category
    from .website.controllers.admin.book_controller import admin_book
    from .website.controllers.admin.user_controller import admin_user
    from .website.controllers.admin.dashboard_controller import admin_dashboard
    from .website.controllers.admin.rating_review_controller import admin_rating_review

    app.register_blueprint(dashboard, url_prefix = '/')
    app.register_blueprint(book, url_prefix = '/book/')
    app.register_blueprint(auth, url_prefix = '/auth/')
    app.register_blueprint(admin_dashboard, url_prefix='/admin/')
    app.register_blueprint(admin_category, url_prefix='/admin/category/')
    app.register_blueprint(admin_book, url_prefix = '/admin/book/' )
    app.register_blueprint(admin_user, url_prefix = '/admin/user/' )
    app.register_blueprint(admin_rating_review, url_prefix ='/admin/rating-review/')

def __register_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .website.schemas.user import User
    
    @login_manager.user_loader
    def load_user(id):
        return next(get_db_context()).query(User).get(UUID(id))