from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
import os
from flask.ext.cors import CORS

application = Flask(__name__)
api=Api(application)
cors = CORS(application, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload_directory')
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root@localhost:3306/horizon'
db = SQLAlchemy(application, session_options={'expire_on_commit': False})
