# -*- coding: utf-8 -*-
from flectra import http

# class MarketingChart(http.Controller):
#     @http.route('/marketing_chart/marketing_chart/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marketing_chart/marketing_chart/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marketing_chart.listing', {
#             'root': '/marketing_chart/marketing_chart',
#             'objects': http.request.env['marketing_chart.marketing_chart'].search([]),
#         })

#     @http.route('/marketing_chart/marketing_chart/objects/<model("marketing_chart.marketing_chart"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marketing_chart.object', {
#             'object': obj
#         })