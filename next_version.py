from flask.ext.restful import Resource
import json
import subprocess
from subprocess import Popen, PIPE

def next_version_node(id):
    print id
    output = subprocess.check_output(['npm','view', id,'version'])
    return {"success":"true","next_version":output.strip()}

def next_version_python(id):
    print id
    output = subprocess.check_output(['pip','list','-o'])
    line=output.split('\n')
    version="No Info"
    for l in line:
        if(l.split(' (')[0]==id):
            version = l.split('Latest: ')[1].split(' [')[0]
            version.strip()
    return {"success":"true","next_version":version}


def next_version_rails(id):
    print id
    output = subprocess.check_output(['gem','list',id,'-all','-r'])
    line=output.split('\n')
    for l in line:
        if(l.split(' (')[0]==id):
            version=l.split(' (')[1].split(',')[0]
    return {"success":"true","next_version":version}


def next_version_php(id):
    return {"success":"false","next_version":"Currently we do not support composer Packages"}

class next_version(Resource):
    def get(self,id,type):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        for er in data['projects']:
            if(er['project']==type):
                language=er['language']
        print language
        if(language=="node"):
            return next_version_node(id)
        if(language=="python"):
            return next_version_python(id)
        if(language=="ror"):
            return next_version_rails(id)
        if(language=="php"):
            return next_version_php(id)
