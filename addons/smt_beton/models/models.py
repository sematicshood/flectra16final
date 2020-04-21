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
    pass


class SmtInvoice(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def action_validate_invoice_payment(self):
        res = super(SmtInvoice, self).action_validate_invoice_payment()
        last_id = self.env['account.payment'].search([], order='id desc')[0].id
        payment = self.env['account.payment'].search([('id', '=', last_id)])
        invoice_id = payment.invoice_ids.id
        amount = payment.amount
        invoices = self.env['account.invoice.line'].search([('invoice_id', '=', invoice_id)])
        all_price = []
        for invoice in invoices:
            price_unit = invoice.price_unit
            all_price.append(price_unit)
        print("cek", all_price, amount)


        

