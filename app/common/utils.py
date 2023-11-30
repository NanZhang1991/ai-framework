"""基本组件"""
import time
from functools import wraps

def timer(module='s',logger=None):
    """time-consuming computation decorator"""
    def wrapper(func):
        def insert_message(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            cost_time = time.perf_counter() - start_time
            if logger:
                logger.info("module:%s \n function:%s, time consuming:%ss",
                            file, func.__name__, cost_time)
            else:
                print(f"module:{module} \n function:{func.__name__},time consuming:{cost_time:.5f}s")
            return result
        return insert_message
    return wrapper


def time_master(func):
    @wraps(func)
    def call_func(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        exec_time = f"{time.time() - start_time :.2f}s"
        print(f'{func.__name__} function exec time {exec_time}')
        # logger.info('%s function exec time %s', func.__name__, exec_time)
        return res
    return call_func


class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Function execution timed out")


def timeout_monitor(time_limit):
    """Timeout detection decorator"""
    def wrapper(func):
        def call_func(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(time_limit)
            try:
                res = func(*args, **kwargs)
                # 如果函数在time_limit内完成，取消定时器
                signal.alarm(0)
                return res 
            except TimeoutException as e:
                raise e
            finally:
                pass
        return call_func
    return wrapper

if __name__=="__main__":
    @timer()
    def test():
        time.sleep(2)
        return 1

    print(test())
