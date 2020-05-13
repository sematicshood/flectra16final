# -*- coding: utf-8 -*-
from flectra import http

# class SmtGajian(http.Controller):
#     @http.route('/smt_gajian/smt_gajian/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smt_gajian/smt_gajian/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smt_gajian.listing', {
#             'root': '/smt_gajian/smt_gajian',
#             'objects': http.request.env['smt_gajian.smt_gajian'].search([]),
#         })

#     @http.route('/smt_gajian/smt_gajian/objects/<model("smt_gajian.smt_gajian"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smt_gajian.object', {
#             'object': obj
#         })