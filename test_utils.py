#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TestData(object):
    SEARCH =  [
        {
            'commits_url': 'commits_url{}{{'.format(i),
            'full_name': 'fname{}'.format(i),
            'name': 'name{}'.format(i),
            'created_at': 'date{}'.format(i),
            'owner': {
                'html_url': 'html_url{}'.format(i),
                'avatar_url': 'avatar_url{}'.format(i),
                'login': 'login{}'.format(i),
                }
        } for i in range(5)
    ]
    COMMITS = [
        [
            {
                'sha': 'sha{}'.format(i),
                'commit': {
                    'message': 'message{}'.format(i),
                    'author': {
                        'name': 'author_name{}'.format(i)
                    }
                }
            }
        ] for i in range(5)     
    ]