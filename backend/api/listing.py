from flask import Flask, abort, request
from flask_restful import Resource, Api
from api.config import readCfg 
from api.config.readCfg import read_config
import json
from flask_restplus import Api, Resource, fields
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from pymongo import MongoClient

config = read_config(['api/config/local.properties'])

app = Flask(__name__)
api = Api(app, version='1.0', title='Managed JH',
    description='Just a framework for JH as a service',
)

apiuser=config.get('dev','api.u')
p=config.get('dev','api.p')
auth = HTTPBasicAuth()

users = {
    apiuser : generate_password_hash(p)
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False



class Dashboard(Resource):
    @auth.login_required
    
    def get(self):
        input_file = open ('api/config/dashboard.json')
        json_array = json.load(input_file)
        print(json_array)
        return json_array

class KeepAlive(Resource):

    def get(self):
        return "OK"



api.add_resource(Dashboard, '/dashboard')
api.add_resource(KeepAlive, '/keepalive')

