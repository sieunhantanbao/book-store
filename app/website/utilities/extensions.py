from cgi import FieldStorage
import os
from werkzeug.utils import secure_filename
import uuid
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