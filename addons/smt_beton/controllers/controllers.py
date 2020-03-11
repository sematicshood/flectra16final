# -*- coding: utf-8 -*-
from flectra import http
from flectra.http import request
from datetime import datetime

class SmtBeton(http.Controller):

    @http.route('/smt_beton/smt_beton/', auth='user')
    def index(self):
        return "Hello, world"