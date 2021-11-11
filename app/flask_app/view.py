
import os
from pathlib import Path

from flask import Blueprint, request, send_file, send_from_directory, make_response, jsonify, url_for, current_app
from ..common.log import logger
from ..common.exception import CustomException
from ..config.config import LOG_DIR
from ..celery_app.task import get_start, get_status

logger = logger(os.path.join(LOG_DIR, 'view.log'), __name__)
app_name = Blueprint("/app_name", __name__, url_prefix='/app_name')

@app_name.route('/')
def test():
    logger.info('OK')
    return '200' 

@app_name.route('/task_start', methods=['POST'], strict_slashes=False)
def task_start():
    data = request.get_json(force=True)
    logger.info(f"request data---------\n  data:{data}")
    # Asynchronous tasks
    task = get_start.apply_async([data]) # Pass the parameter as a list  
    task_id = task.task_id
    print('---------------', task_id)
    return make_response(jsonify(code=200, data={"task_id":task_id}, msg='success'))


@app_name.route('/task_status', methods=['GET'])
def task_status():
    task_id = request.args.get('task_id')
    my_dict = get_status(task_id)
    if my_dict.get('data')==None:
        my_dict['data'] = []
    return make_response(jsonify(my_dict))

    
