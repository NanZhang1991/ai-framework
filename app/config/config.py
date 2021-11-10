import os 
from pathlib import Path
from functools import wraps
from ..common.dataload import load_json
'''
Configure config through the .py file
'''

def convert_path(path):
        read_path = os.path.join(os.getcwd(), path)
        read_path = Path(path).as_posix()
        return read_path

config_path = 'app/config/config.json'
config = load_json(config_path)
UPLOAD_FOLDER = config.get('UPLOAD_FOLDER')
OUTPUT_FOLDER = config.get('OUTPUT_FOLDER')
LOG_DIR = config.get('LOG_DIR')

deploy_path = 'app/config/deploy.json'
deploy_config = load_json(deploy_path)
DOWNLOAD_FILE_IP = deploy_config.get('download_file_ip') 
UPLOAD_FILE_IP = deploy_config.get('upload_file_ip')



