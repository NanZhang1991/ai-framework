import json
import os
import stat
from pathlib import Path

flags = os.O_RDWR | os.O_CREAT
mode = stat.S_IRUSR | stat.S_IWUSR

def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        dic = json.load(f)
    return dic

class Dataload:
@staticmethod   
def load_json(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        dic = json.load(f)
    return dic

@staticmethod
def to_json(dic, fp):
    with os.fdopen(os.open(file_path, flags, mode), 'w') as f:
        json.dump(dic, f, indent=2)  


def convert_path(path):
    real_path = os.path.join(os.getcwd(), path)
    real_path = Path(real_path).as_posix()
    return real_path

if __name__=='__main__':
    config_path = convert_path('app/config/config.json')
    config = load_json(config_path)
    print(config)

