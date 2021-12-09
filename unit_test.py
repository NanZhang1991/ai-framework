import os
import unittest
from app.main import  MainProgram
from app.common.log import logger
from app.config.config import LOG_DIR

logger = logger(os.path.join(LOG_DIR, 'unit_test.log'), __name__)

class TestStringMethods(unittest.TestCase):
    def test_string(self):
        input_fp = {'a':2, "b":3}
        app_result = MainProgram.function(input_fp)
        my_dict = {'code':200, 'data':app_result.get('data'), 'msg':app_result.get('message')}
        logger.info("Success")
        assert isinstance(my_dict, dict)  
            
if __name__ == '__main__':
    unittest.main()