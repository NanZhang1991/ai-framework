def timer(message,log):
    def wrapper(func):
        def insert_message(*args, **kwargs):
            t1= time.time()
            result = func(*args, **kwargs)
            t2 =time.time()
            cost_time = t2-t1
            log.info(f"函数{func.__name__}， {message} 花费时间：{cost_time}秒")
            return result
        return insert_message
    return wrapper
