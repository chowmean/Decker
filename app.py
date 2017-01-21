from resources import application
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from resources import *
import urls

application.debug=True;
if __name__ == '__main__':
    application.run(host='0.0.0.0',port=8091)
