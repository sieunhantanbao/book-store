from cgi import FieldStorage
from functools import wraps
import os
from flask import request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
import uuid
from app import redis_client

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in os.environ['ALLOWED_EXTENSIONS']
           
def upload_file(file: FieldStorage):
    filename = secure_filename(file.filename)
    file_name = f'{uuid.uuid4()}_{filename}'
    file_path = os.path.join(ROOT_DIR, os.environ['UPLOAD_FOLDER'], file_name)
    file.save(file_path)
    return file_name

def remove_file(file_name: str):
    file_path = os.path.join(ROOT_DIR, os.environ['UPLOAD_FOLDER'], file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

def clear_redis_cache(cache_keys: list):
    try:
        for key in cache_keys:
            if redis_client.exists(key):
                redis_client.delete(key)
    except Exception as e:
        print(e)

def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False

def is_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view
        