#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, request, Response, render_template
from ratelimit import RateLimitException
from constants import HOST, PORT
from navigator import Navigator


class Server(object):
	
    def __init__(self, host=HOST, port=PORT):
        self._host = host
        self._port = port
        self._app = Flask(__name__)
        self._add_routes()
        self._navigator = Navigator()

    def index(self):
        msg = ('Currently the only supported API endpoint is:\n\n'
                'GET /navigator?search_term=<search_term>\n')
        return msg, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    def navigator(self):
        search_term = request.args.get('search_term')
        if not search_term:
            return self._response(400, {'error': 'you must provide a search_term param'})

        try:
            repos = self._navigator.lookup(search_term)
            return self._template(search_term, repos)
        except RateLimitException:
            return self._response(429, {'error': 'github api limit reached'})

    def _response(self, status, data=None):
        data = data or []
        return Response(json.dumps(data), status=status,
                        mimetype='application/json')    

    def _template(self, search_term, repositories):
        return render_template(
            'template.html', 
            search_term=search_term,
            repositories=repositories, 
            )

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def _add_routes(self):
        self._app.add_url_rule('/', endpoint='index', view_func=self.index)
        self._app.add_url_rule(
            '/navigator', endpoint='navigator', view_func=self.navigator)

    def _test_client(self):
        return self._app.test_client()


if __name__ == '__main__': 
    server = Server()
    server.run()