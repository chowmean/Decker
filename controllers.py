__author__ = 'chowmean'

from flask.ext.restful import Resource
from flask import request
import json
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
            tr[line.split("==")[0]]=line.split("==")[1].strip()
    print tr
    return tr

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
        if(data_to_return['language']=="ROR"):
            return [parseGemfile(data_to_return['path'])]
        if(data_to_return['language']=="Node"):
            return [parseNode(data_to_return['path'])]
        if(data_to_return['language']=="php"):
            return [parsePhp(data_to_return['path'])]
        if(data_to_return['language']=="python"):
            return [parsePython(data_to_return['path'])]
        return {"success":"false"}
