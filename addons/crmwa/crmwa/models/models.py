# -*- coding: utf-8 -*-

from flectra import models, fields, api
from addons.crmwa.crmwa.models.sendwa import Send_Whatsapp

# class crmwa(models.Model):
#     _name = 'crmwa.crmwa'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Accounts(models.Model):
    _name = 'cmrwa.accounts'
    
    no_wa = fields.Char('Nomor whatsapp', required=True)
    no_motor = fields.Char('Nomor motor', required=True)
    tanggal_input = fields.Date('Tanggal input', required=True)
    sudah_diwa = fields.Boolean('Sudah di WA', default=False)


class Sendwa(models.TransientModel):

    _name = 'crmwa.wizards.sendwa'
    _inherit = 'cmrwa.accounts'

    message = fields.Char('Message', required=True)

    @api.multi
    def confirm_button(self):
        message = self.message
        accounts = self.env['cmrwa.accounts'].search([])
        phones = [ account.no_wa for account in accounts if account.no_wa]
        if phones:
            sender = Send_Whatsapp(phones, message)
            sender.send_post('chat', 'text')