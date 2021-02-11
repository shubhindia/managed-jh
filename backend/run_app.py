from flask import Flask, abort, request
from flask_restful import Resource, Api
import json
from flask_restplus import Api, Resource, fields
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from pymongo import MongoClient
from api.route import api_v1

import logging

app = Flask(__name__)
app.config.from_object(__name__)
app.config["DEBUG"] = True
app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
