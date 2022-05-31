#!/usr/bin/env python3
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


ENV = 'local'
GPU = False


class RequestConfig:
    def __init__(self):
        with open("src/config/app_config.json", encoding='utf-8') as f:
            self.app_config = json.load(f)

    def _headers(self):
        env_type = 'prod' if ENV == 'prod' else 'dev'
        headers = {"tenantID": tenant_id,
                   "appID": app_id}
        return headers

    def _gpu(self):
        headers = self._headers()
        url = self.app_config.get(ENV).get('gpu_url')
        if ENV == "dev":
            x_apig_appcode = self.app_config.get(ENV).get('X-Apig-Appcode')
            headers_x_apig_appcode = {"X-Apig-Appcode": x_apig_appcode}
            headers.update(headers_x_apig_appcode)
        else:
            csb_token = self.app_config.get(ENV).get('csb_token')
            headers_csb = {"csb-token": csb_token}
            headers.update(headers_csb)
        return url, headers

    def _local(self):
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        url = "".join(['http://', ip_addr, ':8080/v1/co'])
        return url

    def _cpu_or_local(self):
        headers = self._headers()
        if ENV == "local":
            url = self._local()
        else:
            url = self.app_config.get(ENV).get('url')
        return url, headers

    def _url_headers(self):
        '''
        Description: get request url, headers
        '''
        if GPU:
            url, headers = self._gpu()
        else:
            url, headers = self._cpu_or_local()
        return url, headers

    def request_res(self, case):
        url, headers = self._url_headers()
        print(f"Authorization: {headers.get('Authorization')}")
        response = requests.post(url=url, headers=headers, json=case)
        res_dict = response.json()
        return res_dict


class NumbersTest(unittest.TestCase):
    def test_even(self):
        """
        Test case
        """
        with open('data/input/test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('data/output/test_result.json', 'r', encoding='utf-8') as f:
            test_result = json.load(f)
        for i, case in enumerate(data):
            with self.subTest(i=i):
                res_dict = RequestConfig().request_res(case)
                # costTime 不做比较
                res_dict.pop('costTime')
                test_result[i].pop('costTime')
                self.assertEqual.__self__.maxDiff = None
                self.assertEqual(res_dict, test_result[i])


def generate_test_result():
    """
    Generate test case result
    """
    with open('data/input/test.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    res_list = []
    for case in data:
        res_dict = RequestConfig().request_res(case)
        res_list.append(copy.deepcopy(res_dict))
    df = pd.DataFrame.from_records(res_list)
    df.to_json('data/output/new_test_result.json',
               orient='records', force_ascii=False)
    print("Complete generate test case result")


if __name__ == '__main__':
    # ENV can be in ['local', 'dev', 'prod']
    ENV = 'dev'
    GPU = False
    generate_test_result()
    unittest.main()
