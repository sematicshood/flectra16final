# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions


class invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    printer_data = fields.Text(string="Printer Data", required=False, )
    nopol = fields.Text(string="No Polisi", required=False, )
    mekanik = fields.Text(string="Mekanik", required=False, )
    type_motor = fields.Text(string="Type Motor", required=False, )
    saran_mekanik = fields.Text(string="Saran Mekanik", required=False, )
    km_berikutnya = fields.Text(string="KM Berikutnya", required=False, )

    @api.one
    @api.constrains('mekanik')
    def _check_mekanik(self):
        if not self.mekanik and self.user_sa and self.user_fi and self.user_kas and self.user_pm:
            raise exceptions.ValidationError("Data Petugas Tidak boleh kosong !!!")

    @api.constrains('user_sa')
    def _check_sa(self):
        if not self.user_sa:
            raise exceptions.ValidationError("Data Petugas Tidak boleh kosong !!!")

    @api.constrains('user_fi')
    def _check_fi(self):
        if not self.user_fi:
            raise exceptions.ValidationError("Data Final Inspeksi Tidak boleh kosong !!!")

    @api.constrains('user_kas')
    def _check_fi(self):
        if not self.user_kas:
            raise exceptions.ValidationError("Data Kasir Tidak boleh kosong !!!")

    @api.constrains('user_pm')
    def _check_fi(self):
        if not self.user_pm:
            raise exceptions.ValidationError("Data Partman Tidak boleh kosong !!!")

    @api.multi
    def generate_printer_data(self):
        so = self.env['sale.order'].sudo().search([
            ('name', '=', self.origin)])
        self.nopol = so.x_nopol
        self.mekanik = so.mekanik_id.name
        self.user_sa = so.x_user_sa.name
        self.user_fi = so.checker_id.name
        self.user_kas = so.x_kasir.name
        self.user_pm = so.x_partman.name
        self.km_berikutnya = int(so.km_masuk) + 2000
        self.saran_mekanik = so.x_saran_mekanik
        self.type_motor = so.unitPelanggan.jenisKendaraan.name
        tpl = self.env['mail.template'].search(
            [('name', '=', 'Dot Matrix Invoice')])
        data = tpl.render_template(
            tpl.body_html, 'account.invoice', self.id, post_process=False)
        self.printer_data = data

    @api.multi
    def action_invoice_cancel(self):
        self.printer_data = ''
        return super(invoice, self).action_cancel()

    @api.multi
    def action_invoice_open(self):
        res = super(invoice, self).action_invoice_open()
        self.generate_printer_data()
        return res

class addFieldInvoice(models.Model):
    _inherit = 'account.invoice'

    user_sa = fields.Char(string="Service Advisor", required=False, )
    user_fi = fields.Char(string="Final Check", required=False, )
    user_pm = fields.Char(string="Partman", required=False, )
    user_kas = fields.Char(string="Kasir", required=False, )
