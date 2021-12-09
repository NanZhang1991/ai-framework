from .algorithm.math_utils import calculate
import pandas as pd 
import os
import datetime
from .config.config import OUTPUT_FOLDER

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
        df.to_excel(os.path.join(OUTPUT_FOLDER, excel_name))
        if data:
            result_dict['data'] = excel_name
            result_dict['message'] ='Program processing completed'
        else:
            result_dict['message'] = 'Nothing found'
        return result_dict
