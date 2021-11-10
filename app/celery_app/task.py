from celery.result import AsyncResult
from celery import Celery
from ..common.exception import CustomException
from ..common.dataload import ZipHanding
from ..common.format_chick import FileCheck
from ..config.config import UPLOAD_FOLDER, OUTPUT_FOLDER, DOWNLOAD_FILE_IP, UPLOAD_FILE_IP
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

    message = {}    
    docx_chick = FileCheck(['zip'])
 
    params = {'fileId': file_id}
    file_url_text = requests.get(DOWNLOAD_FILE_IP, params=params).text
    file_url_dict = json.loads(file_url_text)
    print()
    if file_url_dict.get('data'):
        file_url = file_url_dict.get('data').get('fileUrl')
        message['getFileMsg'] = file_url_dict.get('msg')
        content = requests.get(file_url).content
        if docx_chick.allowed_file(file_url) =='zip':
            fn = file_id + '.zip'
            input_fp = os.path.join(UPLOAD_FOLDER, fn)
            input_fp = Path(input_fp).as_posix()
            with open(input_fp, 'wb') as f:
                f.write(content)
            app_result = MainProgram.calculate(input_fp) # main function
            my_dict = {'code':200, 'data':app_result.get('data'), 'msg':app_result.get('message')}
        else:
            my_dict = {'code':201, 'msg':'File format error'}
            return my_dict

    else:
        my_dict = {'code':205, 'msg':'File not found'}
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


    
