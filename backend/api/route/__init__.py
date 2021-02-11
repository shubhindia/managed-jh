from flask.blueprints import Blueprint
from flask import Flask, request, jsonify
import json
import logging
import os
from os import path
import docker
api_v1 = Blueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')
name = "route"
__all__ = ["api_v1"]

logger = logging.getLogger()
logger.setLevel(int(os.getenv("LOGLEVEL", 10)))

@api_v1.route('/keepalive', methods=['GET'])
def keepalive():
    return "Ok"

@api_v1.route('/dashboard', methods=['GET'])
def dashboard():
    resp = json.dumps([{
    "title": "Managed JH",
    "version": "1.0.0"
    }])
    print(resp)
    return resp

@api_v1.route('/create_jh_instance', methods=['POST'])
def create_jh_instance():

    client = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
    request_data = request.get_json()
    name = request_data['name']
    base_dir = '/home/shubhcyanogen/Work/RND/managed-jh-instances'
    user_dir = name
    dir_path = os.path.join(base_dir, user_dir)
    mode = 0o777
    if path.exists(dir_path):
        return jsonify({"Error": "Instance already exists"})
    
    else:
        os.mkdir(dir_path, mode=mode)
    instance_name = str(name) + '-managed-jh-instance'

    volumes = {path:{'bind': '/home/jovyan/work', 'mode': 'rw'}}
    container = client.containers.run('jupyter/scipy-notebook',detach=True, publish_all_ports=True,
                                    volumes=volumes, name=instance_name)

    for n,line in enumerate(container.logs(stream=True)):
        print(n)
        print(line.strip())
        if n == 15:

            token_url = line.strip()
            break
        

    jh_token = str(token_url).split("=")[-1].replace("'","")

    container = client.containers.get(container_id=instance_name)

    port = container.__dict__['attrs']['NetworkSettings']['Ports']['8888/tcp'][0]['HostPort']

    url = 'localhost:' + port + '/?token=' + jh_token

    res = {"instance_url": url}
    return json.dumps(res)
