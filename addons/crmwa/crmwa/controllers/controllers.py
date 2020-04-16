# -*- coding: utf-8 -*-
from flectra import http
from datetime import datetime

class Crmwa(http.Controller):
    @http.route('/crmwa/crmwa/', auth='public')
    def index(self, **kw):
        return http.request.render('crmwa.action_course_list', {
        })

    @http.route('/crmwa/get_input/', auth='public', website=True)
    def get_input(self, **kw):
        return http.request.render('crmwa.account_input', {
        })

    @http.route('/crmwa/post_input/', auth='public', website=True)
    def post_input(self, **kw):
        nomor_hp = http.request.params.get('nomor_hp')
        nomor_motor = http.request.params.get('nomor_motor')
        if not nomor_hp or not nomor_hp.isdigit():
            return 'nomor hp tidak boleh kosong atau nomor hp tidak valid'      
        if not nomor_motor:
            return 'nomor motor tidak boleh kosong'
        vals = {
            'no_wa':nomor_hp,
            'no_motor':nomor_motor,
            'tanggal_input':datetime.now()
        }
        new_account = http.request.env['cmrwa.accounts'].sudo().create(vals)
        if not new_account:
            return 'Input gagal'

        Accounts = http.request.env['cmrwa.accounts']
        return http.request.render('crmwa.accounts_data', {
            'accounts': Accounts.search([])
        })


#     @http.route('/crmwa/crmwa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crmwa.listing', {
#             'root': '/crmwa/crmwa',
#             'objects': http.request.env['crmwa.crmwa'].search([]),
#         })

#     @http.route('/crmwa/crmwa/objects/<model("crmwa.crmwa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crmwa.object', {
#             'object': obj
#         })