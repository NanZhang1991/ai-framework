"""基本组件"""
import time


def timer(file=__file__, logger=None):
    """time-consuming computation decorator"""
    def wrapper(func):
        def insert_message(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time()
            cost_time = t2-t1
            if logger:
                logger.info("module:{} \n function:{}, time consuming:{}s".format(file, func.__name__, cost_time))
            else:
                print("module:{} \n function:{}, time consuming:{:.5f}s".format(file, func.__name__, cost_time))
            return result
        return insert_message
    return wrapper

if __name__=="__main__":
    @timer()
    def test():
        time.sleep(2)
        return 1

    print(test())
