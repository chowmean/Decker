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

#from flask.ext.pymongo import PyMongo
#from resources import mongo
from bson import json_util
from pymongo import MongoClient



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
            try:
                tr[line.split("==")[0]]=line.split("==")[1].strip()
            except:
                print "skipping"
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

class VulnerabilityInfoCPE(Resource):
    def get(self, target, version):##:cpe:/a:data_general:dg_ux:y2k_patchr4.11mu05
        client = MongoClient()
        db = client.decker
        coll = db.cpe
        #cursor = coll.find({"cpe_2_2": target, "cpe_2_2":  version} })
        target = ".*" + target + ".*"
        version = ".*" + version + ".*"
        #cursor = coll.find({"$and": [{"cpe_2_2":  target}, {"cpe_2_2": version}]})
        cursor = coll.find({"$and" : [{"cpe_2_2": { "$regex": target}},{ "cpe_2_2": { "$regex": version}} ]})
        #cursor = coll.find({"vulnerable_configuration_cpe_2_2": { "$regex": target }})
        print "\n\nversion = "+version+"\n\n"
        print "\n\ntarget = "+target+"\n\n"
        i = 0
        ret = []
        for document in cursor:
            print(json.dumps(document, default=json_util.default))
            ret.insert(len(ret), json.dumps(document, default=json_util.default).strip())
            if i == 10 :
                break
            i += 1
        return ret
        #return json.dumps([doc for doc in mongo.db.cves.find({"vulnerable_configuration_cpe_2_2":/rails:4.2.0/})],separators=(',', ': '))
        #return json.dumps([doc for doc in mongo.db.cvess])
class VulnerabilityInfoCVES(Resource):
    def get(self, target, version):##:cpe:/a:data_general:dg_ux:y2k_patchr4.11mu05
        client = MongoClient()
        db = client.decker
        coll = db.cves
        target = ".*" + target + ".*"
        version = ".*" + version + ".*"
        cursor = coll.find({ "$and" : [{"vulnerable_configuration_cpe_2_2": { "$regex": target }}, {"vulnerable_configuration_cpe_2_2": { "$regex": version}}]})
        #cursor = coll.find({"vulnerable_configuration_cpe_2_2": { "$regex": target }})
        print "\n\nversion = "+version+"\n\n"
        print "\n\ntarget = "+target+"\n\n"
        i = 0
        ret = []
        for document in cursor:
            print(json.dumps(document, default=json_util.default))
            ret.insert(len(ret), json.dumps(document, default=json_util.default).strip())
            if i == 10 :
                break
            i += 1
        return ret
        #return json.dumps([doc for doc in mongo.db.cves.find({"vulnerable_configuration_cpe_2_2":/rails:4.2.0/})],separators=(',', ': '))
        #return json.dumps([doc for doc in mongo.db.cvess])


class testClass(Resource):
    def get(self):
        client = MongoClient()
        db = client.decker
        coll = db.cves
        cursor = coll.find({"vulnerable_configuration_cpe_2_2": { "$regex": "2k_patchr4.11mu05"}})
        print "\n\nsadasdasdasdasdasdasddasdasd\n\n"
        i = 0
        ret = []
        for document in cursor:
            print(json.dumps(document, default=json_util.default))
            ret.insert(len(ret), json.dumps(document, default=json_util.default))
            if i == 10 :
                break
            i += 1
        return ret
        #return json.dumps([doc for doc in mongo.db.cves.find({"vulnerable_configuration_cpe_2_2":/rails:4.2.0/})],separators=(',', ': '))
        #return json.dumps([doc for doc in mongo.db.cvess])

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
        print data_to_return
        if(data_to_return['language']=="ror"):
            return [parseGemfile(data_to_return['path'])]
        if(data_to_return['language']=="node"):
            return [parseNode(data_to_return['path'])]
        if(data_to_return['language']=="php"):
            return [parsePhp(data_to_return['path'])]
        if(data_to_return['language']=="python"):
            return [parsePython(data_to_return['path'])]
        return {"success":"false"}


class VulnerabilityProjectInfoCPE(Resource):
    def get(self,target):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        for er in data['projects']:
            if(er['project']==target):
                data_to_return = er
        print data_to_return
        if(data_to_return['language']=="ror"):
            tr = [parseGemfile(data_to_return['path'])]
        if(data_to_return['language']=="node"):
            tr = [parseNode(data_to_return['path'])]
        if(data_to_return['language']=="php"):
            tr = [parsePhp(data_to_return['path'])]
        if(data_to_return['language']=="python"):
            tr = [parsePython(data_to_return['path'])]
        print "here\n\n"
        print tr
        ret = []
        for a in tr[0]:
            target = a
            version = tr[0][a]
            client = MongoClient()
            db = client.decker
            coll = db.cpe
            #cursor = coll.find({"cpe_2_2": target, "cpe_2_2":  version} })
            target = ".*" + target + ".*"
            version = ".*" + version + ".*"
            cursor = coll.find({"$and" : [{"cpe_2_2": { "$regex": target}},{ "cpe_2_2": { "$regex": version}} ]})
            i = 0
            for document in cursor:
                print(json.dumps(document, default=json_util.default))
                ret.insert(len(ret), json.dumps(document, default=json_util.default).strip())
                if i == 10 :
                    break
                i += 1
            if(i!=0):
                REDISINSTANCE.set(target,REDISINSTANCE.get(target)+1)
        return ret
class VulnerabilityProjectInfoCVES(Resource):
    def get(self,target):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        for er in data['projects']:
            if(er['project']==target):
                data_to_return = er
        print data_to_return
        if(data_to_return['language']=="ror"):
            tr = [parseGemfile(data_to_return['path'])]
        if(data_to_return['language']=="node"):
            tr = [parseNode(data_to_return['path'])]
        if(data_to_return['language']=="php"):
            tr = [parsePhp(data_to_return['path'])]
        if(data_to_return['language']=="python"):
            tr = [parsePython(data_to_return['path'])]
        print tr
        ret = []
        for a in tr[0]:
            target = a
            version = tr[0][a]
            client = MongoClient()
            db = client.decker
            coll = db.cves
            target = ".*" + target + ".*"
            version = ".*" + version + ".*"
            cursor = coll.find({ "$and" : [{"vulnerable_configuration_cpe_2_2": { "$regex": target }}, {"vulnerable_configuration_cpe_2_2": { "$regex": version}}]})
            i = 0
            for document in cursor:
                print(json.dumps(document, default=json_util.default))
                ret.insert(len(ret), json.dumps(document, default=json_util.default).strip())
                if i == 10 :
                    break
                i += 1
            if(i!=0):
                REDISINSTANCE.set(target,REDISINSTANCE.get(target)+1)
        return ret
