#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: main.py
@Time: 2023/07/12 15:28:08
@Version: 1.0
@License: (C)Copyright sunnetech.cn 2023. All rights reserved.
@Desc: File description
@Modify: 2023/07/12
'''
import time
import traceback
from typing import List
from db_work import SqlWork
from logs import get_logger, LogParams
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from utils import FunctionTimedOut
from rec import texts_pun_recorver as main


logger = get_logger(LogParams('log/' + 'main.log', __name__,
                    'debug', "midnight", 1, 31))

app = FastAPI()
db = SqlWork()


class Texts_Info(BaseModel):
    split_id: str
    content: List[str]


def format_result(df):
    keys = ["id", "content"]
    real_keys = [k for k in keys if k in df.columns]
    df = df[real_keys]
    res = {'total': df.shape[0],
           'detail': df.to_dict(orient='records')}
    return res


@asynccontextmanager
async def lifespan(app: FastAPI):
    """mysql定时重连"""
    db.scheduler_task()


def background_operation():
    start_time = time.perf_counter()
    logger.info("Background operation started")
    time.sleep(2)
    cost_time = f'{time.perf_counter() - start_time:.6f}s'
    logger.info("Cost time %s Background operation finished\n", cost_time)


@app.get("/")
async def read_root(background_tasks: BackgroundTasks):
    logger.info('Api test')
    start_time = time.perf_counter()
    background_tasks.add_task(background_operation)
    cost_time = f'{time.perf_counter() - start_time:.6f}s'
    return {"message": "Hello, World!", "cost_time": cost_time}


def _semantic_segmentation(text_info: Texts_Info):
    try:
        start_time = time.time()
        logger.info('%sBegin%s', '-' * 50, '-' * 50)
        split_id = text_info.split_id
        content = text_info.content
        logger.info('text_id %s\n content\n%s',
                    split_id, content)
        res = {"code": 200, "data": [], "info": "success"}
        try:
            df = main(split_id, content)
        except FunctionTimedOut as te:
            db.update_state(split_id)
            raise te
        if not df.empty:  # 如果有结果写入数据库
            db.update_data(df)
            res["data"] = format_result(df)
        else:
            res.update({"info": "No result"})
    except (Exception, BaseException) as e:
        logger.error(traceback.format_exc())
        res = {"code": 500, "data": [], "info": str(e)}
    finally:
        res['cost_time'] = f'{time.time() - start_time:.6f}s'
        logger.info('----result----\n %s', res)
        logger.info('%sFinished%s\n\n', '-' * 50, '-' * 50)
        return JSONResponse(status_code=res.get('code'), content=res)


@app.post('/semantic/segmentation', response_class=JSONResponse)
async def semantic_segmentation(background_tasks: BackgroundTasks,
                                text_info: Texts_Info):
    start_time = time.perf_counter()
    res = {"code": 200, "message": "Request successful"}
    try:
        background_tasks.add_task(_semantic_segmentation, text_info=text_info)
    except (Exception, BaseException) as e:
        logger.error(traceback.format_exc())
        res = {"code": 500,  "message": str(e)}
    cost_time = f'{time.perf_counter() - start_time:.6f}s'
    res['cost_time'] = cost_time
    return JSONResponse(status_code=res.get('code'), content=res)

if __name__ == '__main__':
    uvicorn.run(app='service:app', host='0.0.0.0', port=8116)
