import os 
import logging
from logging import handlers 

def get_logger(fn='log/' + str(os.getpid()) + 'main.log', module_name="main", level=logging.INFO, when="midnight", interval=1, backupCount=31):
    logging.basicConfig()
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)    
    th = handlers.TimedRotatingFileHandler(filename=fn, when=when, interval=interval, backupCount=backupCount, encoding='utf-8')
    th.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    th.setFormatter(formatter)
    th.setLevel(level)
    logger.addHandler(th)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    logger.removeHandler(stream_handler)
    return logger

logger = get_logger()

if __name__ == "__main__":
    logger.debug('Quick zephyrs blow, vexing daft Jim.')
    logger.info('How quickly daft jumping zebras vex.')
    logger.error('unknow')

