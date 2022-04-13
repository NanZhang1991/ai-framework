import json
import unittest
import requests
import socket


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test case
        """
        url = "".join(['http://', IPAddr, ':8080/v1/co'])
        headers = {}
        with open('data/input/test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('data/output/test_result.json', 'r', encoding='utf-8') as f:
            test_result = json.load(f)
        for i, case in enumerate(data):
            with self.subTest(i=i):
                response = requests.post(url=url, headers=headers, json=case)
                res = json.loads(response.text)
                res.pop('costTime')
                test_result[i].pop('costTime')
                self.assertEqual.__self__.maxDiff = None
                self.assertEqual(res, test_result[i])


if __name__ == '__main__':
    unittest.main()
