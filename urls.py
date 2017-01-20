from resources import *
from flask.ext.restful import Resource
from controllers import *


api.add_resource(testClass,'/api/testAPI')
api.add_resource(repositories,'/api/repositories')
api.add_resource(dependencies,'/api/get_dependencies','/api/get_dependencies/<string:id>')
api.add_resource(next_version,'/api/next_version','/api/next_version/<string:id>/<string:type>')
api.add_resource(login,'/githubcallback/','/githubcallback/')
api.add_resource(get_name,'/get_name/','/get_name/<string:key>')
