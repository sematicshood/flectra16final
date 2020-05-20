# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra import exceptions
import uuid
from datetime import datetime

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

    x_kode_konsumen = fields.Char("Kode Konsumen", default=str(uuid.uuid4().fields[-1])[:5])

    # noktp = fields.Char("NO ktp")
    # nosiup = fields.Char()
    # notdp = fields.Char()
    # noptkp = fields.Char()


class AddFieldSaleorder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def len_jumlah_produk(self):
        for rec in self:
            if rec.order_line:
                rec.x_jumlah_produk = len(rec.order_line)

    jaraklokasicor = fields.Float(string='Jarak Ke Lokasi' ,default='')
    x_kode_konsumen_so = fields.Char(related='partner_id.x_kode_konsumen', string='Kode Konsumen', default='')
    x_nama_proyek = fields.Char(string='Nama Proyek', required=True, default='')
    x_tanggal_cor = fields.Date('Tanggal Pengecoran', required=True, default=lambda self: fields.datetime.now())
    x_mutu_bahan = fields.Char(string='Mutu Bahan', required=True, default='')
    x_jumlah_produk = fields.Char(string='Jumlah Dipesan', default='')
    x_metode_pembayaran = fields.Char(string='Metode Pembayaran' ,default='')
    x_is_pajak = fields.Boolean('Pajak/Tidak', default=False)
    x_with_pompa = fields.Char(string='Pakai Pompa Long/Short' ,default='')


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


class ChangeScrum(models.Model):
    _inherit = 'project.sprint'



class UpdateScrum(models.Model):
    _name = 'smt.update.scrum'

    @api.multi
    def add_sale_order(self):
        sales = self.env['sale.order'].search([])
        for sale in sales:
            user_id = sale.user_id
            partner_id = sale.partner_id
            company_id = sale.company_id
            lines = sale.order_line
            for line in lines:
                line_id= line.id
                item = self.env['sale.order.line'].search([('id', '=', line_id)])
                name = item.name
                project_name = self.env['project.project'].search([('name', '=', name),('user_id','=', user_id.id)])
                if not project_name:
                    data = {"name":name,
                        "partner_id":partner_id.id,
                        "user_id":user_id.id,
                        "company_d":company_id.id}
                    self.env['project.project'].create(data)



class invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    printer_data_jormix = fields.Text(string="Printer Data", required=False, )
    no_bukti_pengiriman = fields.Char("No. Bukti Pengiriman", default=str(uuid.uuid4().fields[-1])[:5])
    name_perusahaan = fields.Text(string="Dipasok Oleh", default='JORMIX')
    alamat_perusahaan = fields.Text(string="alamat_perusahaan", default='')
    telpon_perusahaan = fields.Text(string="telpon_perusahaan", default='')
    nama_konsumen = fields.Text(string="Nama Pembeli", required=False, defaulf='')
    nama_proyek = fields.Text(string="Proyek", required=False, defaulf='')
    mutu_produk = fields.Text(string="Mutu", required=False, defaulf='')
    kode_produk = fields.Text(string="Kode Produk", required=False, defaulf='')
    slump = fields.Text(string="Slump", required=False,defaulf='' )
    volume = fields.Text(string="Volume", required=False, defaulf='' )
    total_volume = fields.Text(string="Total", required=False, defaulf='')
    no_truk = fields.Text(string="No Truk", required=False, defaulf='')
    tanggal_pengiriman = fields.Datetime.now()

    @api.multi
    def generate_printer_data_jormix(self):
        print("cekk", self.origin)
        so = self.env['sale.order'].sudo().search([
            ('name', '=', self.origin)])

        self.alamat_perusahaan = "Monjali St No.30A, Nandan, Sariharjo, Ngaglik, Sleman Regency, Special Region of Yogyakarta 55581"
        self.telpon_perusahaan = "(0274) 625014"
        self.nama_konsumen = self.partner_id.name
        self.nama_proyek = so.x_nama_proyek
        self.mutu_produk = so.x_mutu_bahan
        self.kode_produk = 'Code-123'
        self.slump = 'Slump123'
        self.volume = '123'
        self.total_volume = '123'
        self.no_truk = 'ABC123'
        tpl = self.env['mail.template'].search(
            [('name', '=', 'Dot Matrix Invoice Jormix')])
        data = tpl.render_template(
            tpl.body_html, 'account.invoice', self.id, post_process=False)
        self.printer_data_jormix = data


    @api.multi
    def action_invoice_open(self):
        res = super(invoice, self).action_invoice_open()
        self.generate_printer_data_jormix()
        return res


    @api.multi
    def action_invoice_cancel(self):
        self.printer_data_jormix = ''
        return super(invoice, self).action_cancel()