# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra import exceptions


class SmtBeton(models.Model):
    _name = 'smt_beton.smt_beton'

    versi = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100


class AddFieldResPartner(models.Model):
    _inherit = 'res.partner'

    noktp = fields.Char()
    nosiup = fields.Char()
    notdp = fields.Char()
    noptkp = fields.Char()


class AddFieldSaleorder(models.Model):
    _inherit = 'sale.order'

    jaraklokasicor = fields.Float()

class ValidateSeven(models.Model):
    _inherit = 'stock.picking'

    test = fields.Char("Oke")

    @api.multi
    def button_validate(self):
        super(ValidateSeven, self).button_validate()
        self.generate_stoke_move()

    def generate_stoke_move(self):
        stocks = self.env['stock.move'].search([])
        cek = []
        for stock in stocks:
            reserved_availability = stock.reserved_availability
            stock.quantity_done = 7
            if reserved_availability:
                stock.reserved_availability = stock.reserved_availability - 7
                cek.append(stock.reserved_availability)

class AddPriority(models.Model):
    _inherit = 'product.template'

    addpriority = fields.Selection([('1', '1'),
                                ('2', '2'),
                                ('3','3'),
                                ('4','4')],
                                string='Prioritas')