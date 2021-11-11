import json
import pandas as  pd
from ast import literal_eval
import os
from pathlib import Path

def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        dic = json.load(f)
    return dic

def load_task(fp):
    task_df = pd.read_csv(fp, encoding='utf-8', dtype={'code':int})
    task_df['data'] = task_df['data'].apply(literal_eval)
    task_df['msg'] = task_df['msg'].apply(literal_eval)
    return task_df 

def convert_path(path):
    real_path = os.path.join(os.getcwd(), path)
    real_path = Path(real_path).as_posix()
    return real_path

if __name__=='__main__':
    config_path = convert_path('app/config/config.json')
    config = load_json(config_path)
    print(config)

