#!/usr/bin/ENV python3
# -*- encoding: utf-8 -*-
'''
@File: unit_test.py
@Time: 2022/04/20 23:27:44
@Version: 1.0
@License: (C)Copyright Huawei Technologies Co., Ltd. 2022. All rights reserved.
@Desc: 单元测试
@Modify: 2022/04/20
'''
import json
import copy
import socket
import unittest
import requests
import pandas as pd


def _request_config():
    '''
    Description: get request url, headers
    '''

    with open("src/config/app_config.json", encoding='utf-8') as f:
        app_config = json.load(f)
    headers_token = {"sm-token": app_config.get(ENV).get('csb_token')}
    headers = {"headers_token": headers_token}

    if ENV == 'local':
        # 本地url从本地获取
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        url = "".join(['http://', ip_addr, ':8080/v1/co'])
    else:
        url = app_config.get(ENV).get('url')

    return url, headers


class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test case
        """
        with open('data/input/test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('data/output/test_result.json', 'r', encoding='utf-8') as f:
            test_result = json.load(f)
        url, headers = _request_config()
        for i, case in enumerate(data):
            with self.subTest(i=i):
                response = requests.post(
                    url=url, headers=headers, json=case)
                res_dcit = response.json()
                res_dict.pop('costTime')
                test_result[i].pop('costTime')
                self.assertEqual.__self__.maxDiff = None
                self.assertEqual(res_dict, test_result[i])

    def test_result(self):
        """
        Generate test case result
        """
        with open('data/input/test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        url, headers = _request_config()
        res_list = []
        for i, case in enumerate(data):
            with self.subTest(i=i):
                res_dict = requests.post(
                    url=url, headers=headers, json=case).json()
                # gpu 环境需要去掉结的一层 {"success": true, "msg": "", "result": {...}}
                res_dict = res_dict.get('result') if GPU else res_dict
                res_list.append(copy.deepcopy(res_dict))
        df = pd.DataFrame.from_records(res_list)
        df.to_json('data/output/new_test_result.json',
                   orient='records', force_ascii=False)


if __name__ == '__main__':
    # ENV can be in ['local', 'dev', 'prod']
    ENV = 'dev'
    unittest.main()
