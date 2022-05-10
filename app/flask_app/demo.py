import platform
from flask import Flask, request, jsonify, make_response, url_for, redirect
from flask_cors import CORS

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources=r'/*')


@app.route('/v1/co', methods=['POST'], strict_slashes=False)
def main():
    data = request.get_json()
    service_name = data.get('service_name')
    print(service_name)
    return redirect(url_for(service_name), code=307)


@app.route('/v1/co/<service_name>', methods=['POST'], strict_slashes=False)
def main_0(service_name):
    print(service_name)
    print(redirect(url_for(service_name)))
    return redirect(url_for(service_name), code=307)


@app.route('/v1/co/service_test', methods=['POST'], strict_slashes=False)
def service_demo():
    return make_response(
        jsonify('service_demo post port test was successful!'), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
