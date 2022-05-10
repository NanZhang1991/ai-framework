#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: log.py
@Time: 2022/04/18 19:55:24
@Version: 1.0
@License: (C)Copyright Huawei Technologies Co., Ltd. 2022. All rights reserved.
@Desc: 时间回滚日志
'''
import os
import collections
import logging
from logging import handlers

LogParams = collections.namedtuple('LogParams',
                                   ['fn', 'module_name',
                                    'level', 'when', 'interval',
                                    'backup_count'])
log_params = LogParams('log/' + str(os.getppid()) + 'main.log', "main",
                       logging.INFO, "midnight", 1, 31)


def get_logger(log_params=log_params):
    logging.basicConfig()
    log = logging.getLogger(log_params.module_name)
    log.setLevel(logging.DEBUG)
    th = handlers.TimedRotatingFileHandler(filename=log_params.fn,
                                           when=log_params.when,
                                           interval=log_params.interval,
                                           backupCount=log_params.backup_count,
                                           encoding='utf-8')
    th.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter('%(asctime)s - %(name)s - \
                                   %(levelname)s - %(message)s')
    th.setFormatter(formatter)
    th.setLevel(log_params.level)
    log.addHandler(th)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_params.level)
    log.addHandler(stream_handler)
    log.removeHandler(stream_handler)
    return log


logger = get_logger()

if __name__ == "__main__":
    logger.debug('Quick zephyrs blow, vexing daft Jim.')
    logger.info('How quickly daft jumping zebras vex.')
    logger.error('unknow')
