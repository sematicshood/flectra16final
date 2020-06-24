# -*- coding: utf-8 -*-
from flectra import http

# class DashboardMarketing(http.Controller):
#     @http.route('/dashboard_marketing/dashboard_marketing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dashboard_marketing/dashboard_marketing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dashboard_marketing.listing', {
#             'root': '/dashboard_marketing/dashboard_marketing',
#             'objects': http.request.env['dashboard_marketing.dashboard_marketing'].search([]),
#         })

#     @http.route('/dashboard_marketing/dashboard_marketing/objects/<model("dashboard_marketing.dashboard_marketing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dashboard_marketing.object', {
#             'object': obj
#         })