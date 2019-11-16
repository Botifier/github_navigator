#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import unittest

from test_utils import TestData
from server import Server
from mock import MagicMock as Mock


class ServerTest(unittest.TestCase):
    
    def setUp(self):
        s = Server()
        s._navigator._search_repos = Mock(return_value=TestData.SEARCH)
        s._navigator._fetch_commits = Mock(return_value=TestData.COMMITS)
        self._app = s._test_client()


    def test_index(self):
        res = self._app.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['content-type'],
                         'text/plain; charset=utf-8')
        self.assertTrue(res.data.startswith(b'Currently'))

    def test_missing_search_term(self):
        res = self._app.get('/navigator')
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(json.loads(res.data), {'error': 'you must provide a search_term param'})

    def test_too_many_requests(self):
        responses = [self._app.get('/navigator?search_term={}'.format(i)) for i in range(11)]
        self.assertEqual(responses[10].status_code, 429)


if __name__ == '__main__':
    unittest.main()