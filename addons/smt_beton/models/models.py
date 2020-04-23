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


class AddChangePrice(models.Model):
    _inherit = 'account.invoice.line'
    price_changed = fields.Float(string='Changed Price')


class SmtInvoice(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def action_validate_invoice_payment(self):
        res = super(SmtInvoice, self).action_validate_invoice_payment()
        last_id = self.env['account.payment'].search([], order='id desc')[0].id
        payment = self.env['account.payment'].search([('id', '=', last_id)])
        invoice_id = payment.invoice_ids.id
        amount = payment.amount
        order='price_subtotal desc'
        invoices = self.env['account.invoice.line'].search([('invoice_id', '=', invoice_id)], order=order )
        prices = [invoice.price_subtotal for invoice in invoices]
        sum_price = sum(prices)
        if amount > sum_price:
            return         
        #200
        #100,100,25
        res = 0.0
        for prior, invoice in enumerate(invoices):
            price_subtotal = invoice.price_subtotal
            invoice.price_changed = price_subtotal
            invoice.name = "Kurang " + str(price_subtotal)

            if prior == 0 and amount:
                if price_subtotal >= amount:
                    res = invoice.price_subtotal - amount
                    invoice.price_changed = res
                    invoice.name = "Kurang " + str(res)
                    if price_subtotal == amount:
                        invoice.name = "Lunas"
                    amount = 0
                else:
                    price_subtotal = invoice.price_subtotal
                    res = amount - price_subtotal
                    invoice.price_changed = 0
                    amount = res
                    invoice.name = "Lunas"
                    

            elif (res != 0.0 or res != 0) and amount:
                price_subtotal = invoice.price_subtotal
                if price_subtotal >= amount:
                    res = price_subtotal - amount
                    invoice.price_changed = res
                    invoice.name = "Kurang " + str(res)
                    if price_subtotal == amount:
                        invoice.name = "Lunas"
                    amount = 0
                else:
                    price_subtotal = invoice.price_subtotal
                    res = amount - price_subtotal
                    invoice.price_changed = 0
                    amount = res
                    invoice.name = "Lunas"



                











        

