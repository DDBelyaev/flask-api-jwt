from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
# from flask_uploads import UploadSet, configure_uploads, ALL
import os

# CONFIGURATION
app = Flask(__name__)
# app.config.from_object(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# In some projects file upload is required
# script_file = UploadSet('scriptfile', ALL)
# UPLOAD_FOLDER = os.path.join(BASEDIR, 'scripts')
# ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsb', 'xlsm'}

app.config['SECRET_KEY'] = '12345'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432' 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# app.config['UPLOADED_SCRIPTFILE_DEST'] = os.path.join(BASEDIR, 'scripts')
# configure_uploads(app, script_file)

# Mail Configuration
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'test@test.com'
app.config['MAIL_PASSWORD'] = '1234'
app.config['MAIL_DEFAULT_SENDER'] = 'test@test.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)

from . import routes
