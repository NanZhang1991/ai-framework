#!/usr/bin/env python
# coding=utf-8
'''
@File: $TM_FILENAME
@Time: $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE $CURRENT_HOUR:$CURRENT_MINUTE:$CURRENT_SECOND
@Version: 1.0
@License: (C)Copyright 2021-2022, Liugroup-NLPR-CASIA
@Desc: 本地批量测试
'''
import json
import copy
import socket
import unittest
import requests
import pandas as pd


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test case
        """
        url = "".join(['http://', IPAddr, ':8080/v1/co'])
        headers = {'csb-token': 'a2b6d9ab-211f-46bb-85bc-752408f9d99f'}
        with open('data/input/test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('data/output/test_result.json', 'r', encoding='utf-8') as f:
            test_result = json.load(f)
        res_list = []
        for i, case in enumerate(data):
            with self.subTest(i=i):
                response = requests.post(url=url, headers=headers, json=case)
                res_dict = json.loads(response.text)
                res_list.append(copy.deepcopy(res_dict))
                res_dict.pop('costTime')
                test_result[i].pop('costTime')
                self.assertEqual.__self__.maxDiff = None
                self.assertEqual(res_dict, test_result[i])
        df = pd.DataFrame.from_records(res_list)
        df.to_json('data/output/new_test_result.json',
                   orient='records', force_ascii=False)


if __name__ == '__main__':
    unittest.main()

