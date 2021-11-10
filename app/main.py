from .algorithm.math_utils import calculate

class MainProgram:
    @staticmethod
    def function(input_fp):
        result_dict = {}
        data = calculate(data=input_fp)
        if data:
            result_dict['data'] = data
            result_dict['message'] ='Review check complete'
        else:
            result_dict['message'] = 'Nothing found'
        return result_dict
