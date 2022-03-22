"""基本组件"""


import time


def timer(file=__file__, logger=None):
    """time-consuming computation decorator"""
    def wrapper(func):
        def insert_message(*args, **kwargs):
            t1= time.time()
            result = func(*args, **kwargs)
            t2 =time.time()
            cost_time = t2-t1
            if logger:
                logger.info(f" module:{file} \n function:{func.__name__}, time consuming:{cost_time}")
            else:
                print(f"module:{file} \n function:{func.__name__}, time consuming:{cost_time}秒")
            return result
        return insert_message
    return wrapper

if __name__=="__main__":
    @timer()
    def test():
        return 1

    print(test())
