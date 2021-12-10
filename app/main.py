from .algorithm.math_utils import calculate
import pandas as pd 
import os
import datetime
from .config.config import OUTPUT_FOLDER
import requests
from .config.config import UPLOAD_FILE_IP

class MainProgram:
    @staticmethod
    def function(data):
        result_dict = {}
        data = calculate(data)
        if data:
            result_dict['data'] = data
            result_dict['message'] ='Program processing completed'
        else:
            result_dict['message'] = 'Nothing found'
        return result_dict

    @staticmethod
    def function_test(data):
        output_fn = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_dict = {}
        data = calculate(data)
        df = pd.DataFrame(data)
        excel_name = "".join([output_fn,".xlsx"])
        output_fp = os.path.join(OUTPUT_FOLDER, excel_name)
        df.to_excel(output_fp)
        # params = {'userId': '0', "userName": 'app'}
        # files = {'file': open(output_fp, 'rb')}
        # response = requests.post(UPLOAD_FILE_IP, params=params, files=files).text
        # res = json.loads(response)
        # {"code":200,"data":{"fileBucketId":"000000007d453c70017d9fc3986c2722","fileName":"招股说明书三元组数据集_内部标注.zip"},"msg":"success"}
        
        if data:
            result_dict['data'] = excel_name
            result_dict['message'] ='Program processing completed'
        else:
            result_dict['message'] = 'Nothing found'
        return result_dict
