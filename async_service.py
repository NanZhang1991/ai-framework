import asyncio
import aiohttp


def check_async(data):
    asyncio.run(proofread_async(data))


async def proofread_async(data, service_ids=[8, 29, 30, 31, 32, 44]):
    '''异步非阻塞'''
    services = {8: proofread_text_8, 29: proofread_text_29,
                30: proofread_text_30, 31: proofread_text_31,
                32: proofread_text_32,  34: proofread_text_34,
                44: proofread_text_44, 45: proofread_text_45}

    '''异步非阻塞'''
    api_tasks = [asyncio.create_task(services.get(i)(data))
                 for i in service_ids]
    for finished_task in asyncio.as_completed(api_tasks):
        await finished_task
    '''异步阻塞'''
    # api_tasks = [services.get(i)(data) for i in service_ids]
    # await asyncio.gather(*api_tasks)

def run_make():
    kafka_obj = KafkaService()
    threads = []
    for msg in kafka_obj.consumption_info('audit_web_check_31', 'proofread'):
        data = json.loads(msg.value)
        logger.info('kafka proofread\n %s\n', data)
        thread = threading.Thread(target=check_async, args=(data,))
        thread.start()
        threads.append(thread)
        # 根据服务容器数量设定并发数
        if len(threads) >= 4:
            logger.info('------4线程------\n%s', threads)
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()


async def proofread_text_8(data):
    url = conf['api_8']
    sid = 8
    logger.info("sid: %s text_id: %s", sid, data['text_id'])
    post_data = {"text_id": data['text_id'], 'content': data['content']}
    try:
        request_json = json.dumps(post_data)
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=request_json,
                                    headers=headers, timeout=3) as resp:
                res = await resp.text()
                logger.info("---result---:\n %s \n\n", str(res))
    except Exception as e:
        logger.error("---error---:\n %s \n\n", str(e))


async def proofread_text_31(data):
    url = conf['api_31']
    sid = 31
    logger.info("sid: %s text_id: %s", sid, data['text_id'])
    post_data = {"text_id": data['text_id'], 'content': data['content']}
    try:
        request_json = json.dumps(post_data)
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=request_json,
                                    headers=headers, timeout=3) as resp:
                res = await resp.text()
                logger.info("---result---:\n %s \n\n", str(res))
    except Exception as e:
        logger.error("---error---:\n %s \n\n", str(e))


async def proofread_text_29(data):
    url = conf['api_29']
    sid = 29
    logger.info("sid: %s text_id: %s", sid, data['text_id'])
    post_data = {"text_id": data['text_id'], 'content': data['content']}
    try:
        request_json = json.dumps(post_data)
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=request_json,
                                    headers=headers, timeout=3) as resp:
                res = await resp.text()
                logger.info("---result---:\n %s \n\n", str(res))
    except Exception as e:
        logger.error("---error---:\n %s \n\n", str(e))
