import platform
from flask import Flask, request, jsonify, make_response, url_for, redirect
from flask_cors import CORS
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources=r'/*')


@app.route('/v1/co', methods=['POST'], strict_slashes=False)
def main():
    # json
    data = request.get_json()
    service_name = data.get('service_name')
    # default code 302 return get request， code 307 return post request
    print(f"{'*'*10} {redirect(url_for(service_name), code=307)} {'*'*10}")
    return redirect(url_for(service_name), code=307)


@app.route('/v1/co/<service_name>', methods=['POST'], strict_slashes=False)
def main_0(service_name):
    # text/json
    data = request.get_data()
    data = json.loads(data)
    data = data.get('service_name')
    print(f"{'*'*10} {data} {'*'*10}")
    return redirect(url_for(service_name))


@app.route('/v1/co/service', methods=['POST'], strict_slashes=False)
def main_1():
    # form-data
    data = request.form.get('data')
    print(f"{'*'*10} {data} {'*'*10}")
    return make_response(jsonify(data), 404)


@app.route('/v1/co/service_test',
           methods=['GET', 'POST'], strict_slashes=False)
def service_demo():
    if request.method == 'GET':
        result = jsonify('service_demo get port test was successful!')
    else:
        result = jsonify('service_demo post port test was successful!')
    return make_response(result, 200)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        app.run(host="0.0.0.0", port=8080, debug=True)
    else:
        app.run(host="0.0.0.0", port=80)