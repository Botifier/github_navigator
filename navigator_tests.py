#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from navigator import Navigator
from mock import MagicMock as Mock
from test_utils import TestData
from ratelimit import RateLimitException


class NavigatorTest(unittest.TestCase):
    
    def setUp(self):
        self._nav = Navigator()
        self._nav._search_repos = Mock(return_value=TestData.SEARCH)
        self._nav._fetch_commits = Mock(return_value=TestData.COMMITS)

    def test_normal_lookup(self):
        results = self._nav.lookup('test')
        self.assertEqual(len(results), 5)
        first = results[0]
        self.assertEqual(set(first.keys()), set([
            'repo_full_name', 
            'name', 
            'created_at',
            'latest_commit',
            'owner_avatar_url',
            'owner_url',
            'owner_login',
            ])
        )
        self.assertEqual(set(first['latest_commit'].keys()), set([
            'message', 
            'hash', 
            'author',
            ])
        )

    def test_lookup_with_no_results(self):
        self._nav._search_repos = Mock(return_value=[])
        results = self._nav.lookup('test')
        self.assertEqual(results, [])
    
    def test_lookup_with_less_than_five_results(self):
        self._nav._search_repos = Mock(return_value=TestData.SEARCH[:4])
        self._nav._fetch_commits = Mock(return_value=TestData.COMMITS[:4])
        results = self._nav.lookup('test')
        self.assertEqual(len(results), 4)

    def test_rate_limit_reached(self):
        with self.assertRaises(RateLimitException):
            res = [self._nav.lookup(i) for i in range(10)]

    def test_bypass_api_limit_for_cached_data(self):
        res = [self._nav.lookup(i) for i in [1]*10]
        self.assertEqual(len(res), 10)


if __name__ == '__main__':
    unittest.main()