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
