#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File: validation.py
@Time: 2022/04/18 20:02:35
@Version: 1.0
@License: (C)Copyright Zhangnan. 2022. All rights reserved.
@Desc: Input data Validation
'''
import re
import uuid


class ValData():
    def __init__(self, data):
        self.data = data

    @staticmethod
    def format_key(string: str):
        '''convert like articleItemId as article_item_id'''
        tokens = ([w.lower() for w in re.split(r'([A-Z][a-z]*)', string) if w])
        res = '_'.join(tokens)
        return res

    @property
    def article_title(self):
        if not self.data.get('articleTitle'):
            raise ValueError('articleTitle is the value that must be entered')
        if not isinstance(self.data['articleTitle'], str):
            raise ValueError('articleTitle must be string type!')
        return self.data['articleTitle']

    @property
    def article_item_id(self):
        if not self.data.get('articleItemId'):
            self.data['articleItemId'] = str(uuid.uuid1())
        if not isinstance(self.data['articleItemId'], str):
            raise ValueError('articleItemId must be string type!')
        return self.data['articleItemId']

    @property
    def content(self):
        if not self.data.get('content'):
            raise ValueError('content is the value that must be entered')
        if not isinstance(self.data['content'], str):
            raise ValueError('content must be string type!')
        return self.data['content']

    @property
    def language(self):
        if not self.data.get('language'):
            raise ValueError('language is the value that must be entered')
        if not isinstance(self.data['language'], str):
            raise ValueError('language must be string type!')
        if self.data['language'] not in {'en-US'}:
            raise ValueError("language value must in {'en-US'}")
        return self.data['language']

    @property
    def token_size(self):
        if self.data.get('tokenSize') is None:
            self.data['tokenSize'] = 150
        if not isinstance(self.data['tokenSize'], int):
            raise ValueError('tokenSize must be an integer type!')
        return self.data['tokenSize']

    @property
    def sim_model(self):
        if not self.data.get('simModel'):
            self.data['simModel'] = 'Jaccard'
        if not isinstance(self.data['simModel'], str):
            raise ValueError('simModel must be string type!')
        if str.title(self.data['simModel']) not in {'Jaccard', 'Simcse'}:
            raise ValueError("simModel value must in {'Jaccard', 'Simcse'}")
        return str.lower(self.data['simModel'])

    @property
    def text_clean_flag(self):
        if not self.data.get('textCleanFlag'):
            self.data['textCleanFlag'] = 'N'
        if not isinstance(self.data['textCleanFlag'], str):
            raise ValueError('textCleanFlag must be string type!')
        if self.data['textCleanFlag'] not in {'N', 'Y'}:
            raise ValueError("textCleanFlag value must in {'N', 'Y'}")
        return self.data['textCleanFlag']


def val_data(data):
    v = ValData(data)
    res_dict = {
                'article_title': v.article_title,
                'article_item_id': v.article_item_id,
                'content': v.content, 'language': v.language,
                'token_size': v.token_size,
                'sim_model': v.sim_model,
                'text_clean_flag': v.text_clean_flag
                }
    return res_dict


class ValHeaders():
    def __init__(self, headers):
        self.data = headers

    @property
    def tenant_id(self):
        if not self.data.get('tenantID'):
            raise ValueError('tenantID is the value that must be entered')
        if not isinstance(self.data['tenantID'], str):
            raise ValueError('tenantID must be string type!')
        return self.data['tenantID']

    @property
    def app_id(self):
        if not self.data.get('appID'):
            raise ValueError('appID is the value that must be entered')
        if not isinstance(self.data['appID'], str):
            raise ValueError('appID must be string type!')
        return self.data['appID']

    @property
    def authorization(self):
        if not self.data.get('authorization'):
            raise ValueError('authorization is the value that must be entered')
        if not isinstance(self.data['authorization'], str):
            raise ValueError('authorization must be string type!')
        return self.data['authorization']


def val_headers(headers: dict):
    v = ValHeaders(headers)
    res_dict = {"tenant_id": v.tenant_id,
                "app_id": v.app_id,
                "authorization": v.authorization}
    return res_dict


if __name__ == '__main__':
    import logging
    import traceback

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s -' +
                        '%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    test_headers = {"tenantID": "com.huawei.finance",
                    "appID": "com.huawei.finance.knowlegra.extraction",
                    "authorization": "asxacacadcandahjklahplkp"}

    test_data = {'articleTitle': 'What Does Russia Want? How Do We Respond?',
                 'articleItemId': '7ea2761264235c6d77315c94412e6efb',
                 'content': 'This is content',
                 'sim_model': 'Jaccard',
                 'language': 'en-US', 'tokenSize': None, 'textCleanFlag': 'N'}

    try:
        headers_dict = val_headers(test_headers)
        logger.info(f"res_headers: {headers_dict}")
        data_dict = val_data(test_data)
        logger.info(f"article_dcit: {data_dict}")
    except Exception as e:
        logger.error(str(e) + traceback.format_exc())
    finally:
        pass
