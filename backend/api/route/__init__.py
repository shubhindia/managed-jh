from flask.blueprints import Blueprint
import json
api_v1 = Blueprint('api_v1', __name__, subdomain='', url_prefix='/api/v1')
name = "route"
__all__ = ["api_v1"]



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