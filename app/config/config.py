import os 
from pathlib import Path
import json 

'''
Configure config through the .py file
'''
    
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        dic = json.load(f)
    return dic
    
def convert_path(path):
    real_path = os.path.join(os.getcwd(), path)
    real_path = Path(real_path).as_posix()
    return real_path


config_path = convert_path('app/config/config.json')
config = load_json(config_path)
INPUT_FOLDER = config.get('INPUT_FOLDER')
OUTPUT_FOLDER = config.get('OUTPUT_FOLDER')
LOG_DIR = config.get('LOG_DIR')

deploy_path = convert_path('app/config/deploy.json')
deploy_config = load_json(deploy_path)
DOWNLOAD_FILE_IP = deploy_config.get('DOWNLOAD_FILE_IP') 
UPLOAD_FILE_IP = deploy_config.get('UPLOAD_FILE_IP')



