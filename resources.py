from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
import os
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo

application = Flask("decker")
application.config['DEBUG'] = True
mongo = PyMongo(application)
api=Api(application)
cors = CORS(application, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload_directory')
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER