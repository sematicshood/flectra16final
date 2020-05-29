# -*- coding: utf-8 -*-
from flectra import http

# class WaAutomation(http.Controller):
#     @http.route('/wa_automation/wa_automation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wa_automation/wa_automation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wa_automation.listing', {
#             'root': '/wa_automation/wa_automation',
#             'objects': http.request.env['wa_automation.wa_automation'].search([]),
#         })

#     @http.route('/wa_automation/wa_automation/objects/<model("wa_automation.wa_automation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wa_automation.object', {
#             'object': obj
#         })