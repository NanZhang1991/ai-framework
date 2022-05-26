import platform
import traceback
import time
from flask import Flask, request, jsonify, make_response, url_for, redirect
from flask_cors import CORS
import json
from app.common.validation import val_headers, val_data
from app.common.log import logger

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources=r'/*')
start_time = time.time()


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
    return make_response(jsonify(data), 200)


@app.route('/v1/co/service_test',
           methods=['GET', 'POST'], strict_slashes=False)
def service_demo():
    logger.info(f"{'='*10} Start {'='*10}")
    global start_time
    start_time = time.time()
    if request.method == 'GET':
        result = 'service_demo get port test was successful!'
        response = make_response(jsonify(result), 200)
    else:
        val_res = _data_validation()
        response = _program(val_res[1]) if val_res[0] else val_res[1]
        logger.info(f"{'='*10} Complete {'='*10} \n")
    return response


def _data_validation():
    """Data validation"""
    try:
        data = request.get_json(force=True)
        headers = request.headers
        headers = val_headers(headers)
        data = val_data(data)
        logger.info(f"tenant_id:{headers.get('tenant_id')}, " +
                    f"app_id:{headers.get('app_id')}, " +
                    f"article_item_id:{data.get('article_item_id')}")
        return True, data
    except Exception as e:
        logger.error(traceback.format_exc())
        result = {"status": 400, "message": str(e),
                  "costTime": '{0:.4f}s'.format(time.time()-start_time),
                  "data": None}
        response = make_response(jsonify(result), 400)
        headers = {'content-type': 'application/json'}
        response.headers = headers
        return False, response
    finally:
        pass
    

# main program
def _program(data):
    try:
        res_dict = summary(data)
        result = {"status": 200, "message": res_dict.get('message'),
                  "costTime": '{0:.4f}s'.format(time.time()-start_time),
                  "data": res_dict.get('summary'),
                  "method": res_dict.get('method')}
        response = make_response(jsonify(result), 200)
    except Exception:
        logger.error(traceback.format_exc())
        result = {"status": 404, "message": traceback.format_exc(),
                  "costTime": '{0:.4f}s'.format(time.time()-start_time),
                  "data": None}
        response = make_response(jsonify(result), 404)
    finally:
        headers = {'content-type': 'application/json'}
        response.headers = headers
    return respons
          

if __name__ == '__main__':
    if platform.system() == 'Windows':
        app.run(host="0.0.0.0", port=8080, debug=True)
    else:
        app.run(host="0.0.0.0", port=80)
