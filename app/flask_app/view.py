
import os
from pathlib import Path

from flask import Blueprint, request, send_file, send_from_directory, make_response, jsonify, url_for, current_app
from ..common.log import logger
from ..common.exception import CustomException
from ..config.config import LOG_DIR
from ..celery_app.task import get_start, get_status, get_start_test
from ..common.format_chick import FileCheck

logger = logger(os.path.join(LOG_DIR, 'view.log'), __name__)
app_name = Blueprint("/app_name", __name__, url_prefix='/app_name')

@app_name.route('/')
def test():
    logger.info('OK')
    return '200' 

@app_name.route('/task/start', methods=['POST'], strict_slashes=False)
def task_start():
    data = request.get_json(force=True)
    logger.info(f"request data---------\n  data:{data}")
    task = get_start.apply_async([data])
    task_id = task.task_id
    print('task_id---------------', task_id)
    return make_response(jsonify(code=200, data={"task_id":task_id}, msg='The request is successful'))

@app_name.route('/task/status', methods=['GET'])
def task_status():
    task_id = request.args.get('task_id')
    my_dict = get_status(task_id)
    if my_dict.get('data')==None:
        my_dict['data'] = []
    return make_response(jsonify(my_dict))

@app_name.route('task/start/test', methods=['POST'], strict_slashes=False)
def task_start_test():
    INPUT_FOLDER = 'app/data/input/'
    docx_chick = FileCheck(['docx'])
    _file = request.files.get('file')
    if _file !=None and docx_chick.allowed_file(_file.filename):
        input_fp = os.path.join(INPUT_FOLDER, _file.filename)
        print(input_fp)
        logger.info(f'input file path -------:{input_fp}')
        _file.save(input_fp)
        task = get_start_test.apply_async([input_fp])  
        task_id = task.task_id
        print('task_id---------------', task_id)
        result = make_response(jsonify(code=200, data={"task_id":task_id}, msg='The request is successful'))
    else:
        result = make_response(jsonify({'code':205, 'message':'The file is missing'}))
    return result

@app_name.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    customer_fn = request.args.get("customer_fn")
    if customer_fn:
        customer_fn = customer_fn
    else:
        customer_fn = filename
    ouptput_directory = os.path.join(os.getcwd(), 'app/data/output/')
    if os.path.exists(os.path.join(ouptput_directory, filename)):
        response = make_response(send_from_directory(ouptput_directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(customer_fn.encode().decode('latin-1'))
    else:
        response = make_response("文件不存在")
    logger.info(f'ouptput_directory ----: {os.path.join(ouptput_directory, filename)}')
    return response