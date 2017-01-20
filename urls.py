from resources import *
from flask.ext.restful import Resource
from controllers import *


api.add_resource(testClass,'/api/testAPI')
api.add_resource(repositories,'/api/repositories')
api.add_resource(dependencies,'/api/get_dependencies','/api/get_dependencies/<string:id>')
