# -*- coding: utf-8 -*-

from flectra import models, fields, api

class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    jenis_motor = fields.Many2one('vehicle.model', string='Tipe Motor')
    no_rangka = fields.Char(default=False, string="No Rangka")
    no_mesin = fields.Char(default=False, string="No Mesin")
    km_masuk =fields.Char(default=False, string="Odometer")
    tahun_motor=fields.Char(default=False, string="Tahun")
    user_cuci = fields.Many2one('res.users', string='User Cuci')
    user_sa = fields.Many2one('res.users', string='Service Advisor')