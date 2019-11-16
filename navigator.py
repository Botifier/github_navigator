#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grequests
import requests

from expiringdict import ExpiringDict
from ratelimit import limits
from constants import ONE_HOUR


class Navigator(object):
    SEARCH_API_URL = 'https://api.github.com/search/repositories'
    
    def __init__(self):
        '''
            search api is not cached by the git api server ==> expiring cache
            however the commits endpoint is cached with etag ==> permanent cache with etags
        '''
        self.cache = ExpiringDict(max_len=5000, max_age_seconds=100)

    def lookup(self, search_term):
        if not self.cache.get(search_term, False):
            self.cache[search_term] = self._api_lookup(search_term)
        return self.cache[search_term]
    
    '''
        Unauthenticated github api calls limit is 60 per hour, api_lookup makes 6 requests per call
        so our limit is 10 calls per hour
    '''
    @limits(calls=10, period=ONE_HOUR)
    def _api_lookup(self, search_term):
        data = []
        repos_data = self._search_repos(search_term)
        for repo in repos_data:
            data.append(
                {
                    'repo_full_name': repo['full_name'],
                    'name': repo['name'],
                    'created_at': repo['created_at'],
                    'owner_url': repo['owner']['html_url'],
                    'owner_avatar_url': repo['owner']['avatar_url'],
                    'owner_login': repo['owner']['login'],
                }
            )

        commits_urls = [ repos_data[x]['commits_url'][:repos_data[x]['commits_url'].index('{')] for x in range(len(data)) ]
        commits_data = self._fetch_commits(commits_urls)

        for i, repo in enumerate(data):
            repo['latest_commit'] = {
                'message': commits_data[i][0]['commit']['message'],
                'author': commits_data[i][0]['commit']['author']['name'],
                'hash': commits_data[i][0]['sha'],
            }
        return data
    
    def _search_repos(self, search_term):
        res = requests.get(self.SEARCH_API_URL, params= {'q':search_term})
        if res.ok:
            repos_list = sorted(res.json()['items'], key=lambda x: x['created_at'], reverse=True)
            return repos_list[:5]
        else:
            return []

    def _fetch_commits(self, commit_urls):
        requests = (grequests.get(url) for url in commit_urls)
        responses = grequests.map(requests)
        if all([res.ok for res in responses]):
            return [commit.json() for commit in responses]
        else:
            return []

    