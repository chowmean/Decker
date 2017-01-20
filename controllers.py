__author__ = 'chowmean'

from flask.ext.restful import Resource
from flask import request
import json
from next_version import *
import requests
from resources import REDISINSTANCE
import string
import random
import flask


def parseGemfile(path):
    tr=dict()
    start=0;
    dep=0;
    f=open(path)
    f=f.read()
    f=f.split('DEPENDENCIES')[1]
    f=f.split('\n')
    for ft in f:
        if(ft!=""):
            ft.strip()
            try:
                tr[ft.split('(')[0].strip()] = ft.split('(')[1].strip().split(')')[0].split('= ')[1]
            except:
                try:
                    tr[ft.split('(')[0].strip()] = ft.split('(')[1].strip().split(')')[0].split('~> ')[1]
                except:
                    print "Left"+ ft
                print "Left"+ ft
    return tr

def parseNode(path):
    with open(path) as json_data_file:
        data = json.load(json_data_file)
    dep=data['dependencies']
    dev_dep=data['devDependencies']
    return {key: value for (key, value) in (dep.items() + dev_dep.items())}

def parsePhp(path):
    with open(path) as json_data_file:
        data = json.load(json_data_file)
    return data['require']

def parsePython(path):
    tr=dict()
    with open(path) as f:
        for line in f:
            tr[line.split("==")[0]]=line.split("==")[1].strip()
    print tr
    return tr


class login(Resource):
    def get(self):
        code=request.args.lists()
        code= code[0][1][0]
        payload = {'client_id': '81e6dc85d40f05e4c2f7', 'client_secret': 'bc5bb3d0423eaa7a10080869ae1061374682caa7','code':code}
        r = requests.post("https://github.com/login/oauth/access_token", data=payload)
        key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(36))
        print key
        REDISINSTANCE.set(key,r.content.split('&')[0].split('=')[1])
        resp = flask.Response('{"code":"'+key+'"}')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class get_name(Resource):
    def get(self,key):
        value=REDISINSTANCE.get(key)
        r=requests.get("https://api.github.com/user?access_token="+value)
        print r.content


class testClass(Resource):
    def get(self):
		return {"data":"hey","succes":True}



class repositories(Resource):
    def get(self):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        return data['projects']


class dependencies(Resource):
    def get(self,id):
        print id
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        for er in data['projects']:
            if(er['project']==id):
                data_to_return = er
        if(data_to_return['language']=="ror"):
            return [parseGemfile(data_to_return['path'])]
        if(data_to_return['language']=="node"):
            return [parseNode(data_to_return['path'])]
        if(data_to_return['language']=="php"):
            return [parsePhp(data_to_return['path'])]
        if(data_to_return['language']=="python"):
            return [parsePython(data_to_return['path'])]
        return {"success":"false"}
