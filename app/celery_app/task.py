from celery.result import AsyncResult
from celery import Celery
from ..common.exception import CustomException
from ..common.format_chick import FileCheck
from ..config.config import INPUT_FOLDER, OUTPUT_FOLDER, DOWNLOAD_FILE_IP, UPLOAD_FILE_IP
from ..main import  MainProgram
import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

from ast import literal_eval

app = Celery('task',  broker='redis://localhost:6379/0', backend='redis://localhost:6379/1') 
# celery.conf.update(app.config)

@app.task
def get_start(data):
    task_id = data.get('taskId')
    file_id = data.get('fileId')
    details = data.get('data')

    zip_chick = FileCheck(['zip'])
 
    params = {'fileId': file_id}
    file_url_text = requests.get(DOWNLOAD_FILE_IP, params=params).text
    file_url_dict = json.loads(file_url_text)

    if file_url_dict.get('data'):
        file_url = file_url_dict.get('data').get('fileUrl')
        content = requests.get(file_url).content
        if zip_chick.allowed_file(file_url):
            fn = file_id + '.zip'
            input_fp = os.path.join(INPUT_FOLDER, fn)
            input_fp = Path(input_fp).as_posix()
            with open(input_fp, 'wb') as f:
                f.write(content)
            app_result = MainProgram.function(input_fp) # main function
            my_dict = {'code':200, 'data':app_result.get('data'), \
                      'msg':{"app_message":app_result.get('message'), "get_file_msg":file_url_dict.get('msg')}}
        else:
            my_dict = {'code':201, 'msg':'File format error'}

    else:
        my_dict = {'code':205, 'msg':'File not found'}
    return my_dict

@app.task
def get_start_test(data): 
    app_result = MainProgram.function_test(data)
    my_dict = {'code':200, 'data':app_result.get('data'), 'msg':{"app_message":app_result.get('message')}}
    return my_dict

def get_status(task_id):
    task = AsyncResult(task_id, app=app)
    # status = task.ready() 
    status = task.state # PENDING FAILURE SUCCESS RETRY STARTED
    my_dict = {}
    result = task.result
    if status == "SUCCESS":
        my_dict = result
        return my_dict
    elif status == "FAILURE":
        my_dict['code']= 204
        my_dict["msg"] = 'Task is %s'%(status)
    else:
        my_dict['code']= 202
        my_dict["msg"] = 'Task is %s'%(status)
    return my_dict


    
