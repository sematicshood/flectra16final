# -*- coding: utf-8 -*-
from flectra import models, fields, api


class bengkel_motor(models.Model):
    _inherit = 'sale.order'

    x_user_cuci = fields.Many2one('res.users', string='Mek. Cuci')
    x_user_sa = fields.Many2one('res.users', string='Service Advisor')
    x_keluhan = fields.Char(string='Keluhan')
    # x_estimasi_waktu = fields.Char()
    # x_nopol = fields.Char()
    # x_type_motor = fields.Char()
    # x_tipe_kendaraan = fields.Char()
    # x_antrian_service = fields.Selection(
    #     [('Reguler', 'Reguler'), ('Pit', 'Pit Express'), ('BS', 'Booking')], string="Antrian Service")
    # x_warna = fields.Char()
    # x_waktu_mulai = fields.Datetime()
    # x_is_reject = fields.Boolean(default=False)
    # x_is_wash = fields.Boolean(default=False)
    # x_duration = fields.Char()
    # x_saran_mekanik = fields.Char()
    # mekanik_id = fields.Many2one('res.users', string='Mekanik')
    # checker_id = fields.Many2one('res.users', string='Final Check')
    # x_kpb = fields.Selection([(1, 1), (2, 2), (3, 3), (4, 4)], string="Type KPB")
    # x_service = fields.Selection(
    #     [('Ringan', 'Ringan'), ('Lengkap', 'Lengkap')], string="Service Type")
    # x_ganti_oli = fields.Boolean(default=False, string="Ganti Oli")
    # x_ganti_part = fields.Boolean(default=False, string="Ganti part")
    # x_turun_mesin = fields.Boolean(default=False, string="Turun Mesin")
    # x_claim = fields.Boolean(default=False, string="Claim")
    # x_job_return = fields.Boolean(default=False, string="Job Return")
    # x_service_kunjungan = fields.Boolean(default=False, string="Service Kunjungan")
    # x_other_job = fields.Boolean(default=False, string="Other Job")
    # x_spesial_program = fields.Boolean(default=False, string="Spesial Program")
    # jenis_motor = fields.Many2one('vehicle.model', string='Tipe Motor')
    # no_rangka = fields.Char(default=False, string="No Rangka")
    # no_mesin = fields.Char(default=False, string="No Mesin")
    # km_masuk =fields.Char(default=False, string="Odometer")
    # tahun_motor=fields.Char(default=False, string="Tahun")
    # user_cuci = fields.Many2one('res.users', string='User Cuci')
    # user_sa = fields.Many2one('res.users', string='Service Advisor')

    @api.multi
    def action_confirm(self):
        self.x_nopol = self.unitPelanggan.name
        self.x_type_motor = self.unitPelanggan.jenisKendaraan.name
        res = super(bengkel_motor, self).action_confirm()
        return res


class saleorderline(models.Model):
    _inherit = 'sale.order.line'

   # x_is_kpb = fields.Selection([('No', " "), ('KPB', "KPB")], default='No'


class products(models.Model):
    _inherit = 'product.template'

    x_is_kpb = fields.Selection([('No', " "), ('KPB', "KPB")], default='No')
    waktu_kerja = fields.Integer()
    waktu_kerja_avg = fields.Integer()
    waktu_kerja_tercepat = fields.Integer()
    waktu_kerja_terlama = fields.Integer()
    # vehicle_models_ids = fields.Many2many(
    #     'fleet.vehicle.model', string='Vehicle Models')
    # minimal_km = fields.Integer('Minimal KM', default=0)
    # registrasi = fields.Boolean('Registrasi', default=False)
    # on_sale = fields.Integer('Terjual', default=0)
    # x_dept = fields.Char('Group Barang')
    # x_ins_counter = fields.Float('Insentif Counter')
    # x_ins_jasa = fields.Float('Insentif Jasa')
    # x_ins_part = fields.Float('Intensif Part')


class invoices(models.Model):
    _inherit = 'account.invoice'

    nomorkartu = fields.Char('Nomor Kartu')
    nmbank     = fields.Char('Nama Bank')
    namadikartu = fields.Char('Nama Di Kartu')
    x_keluhan = fields.Char(string='Keluhan')


class saleaddon(models.Model):
    _inherit = 'sale.order'

    no_antrian = fields.Integer()


class saleaddonjan20(models.Model):
    # addon penambahan field final
    _inherit = 'sale.order'

    x_kasir = fields.Many2one('res.users', string='Kasir')
    x_partman = fields.Many2one('res.users', string='Partman')
    x_part_request = fields.Text(string='Ganti Part')
    x_cr = fields.Boolean(default=False, string="Carbon remover")
    x_si = fields.Boolean(default=False, string="Service Injeksi")


class SaleAddServiceType(models.Model):
    _inherit = 'sale.order'
    #TODO
    # 1 cek ulang tipe service yang ada di update modul bulan desember
    x_service = fields.Selection(
                [('ass', 'KPB'), ('Lengkap', 'Lengkap'), ('LR', 'Light Repair'), ('GO', 'Ganti Oli'),
                 ('GOP', 'Ganti Oli Plus'), ('HR', 'Heavy Repair'), ('JR', 'Job Return'),
                 ('OJ', 'Other Job'), ('CL', 'Claim'),  ('SK', 'Service Kunjungan')], string="Service Type")

class SaleAddServiceType1(models.Model):
    _inherit = 'sale.order'
    #TODO
    # 1 cek ulang tipe service yang ada di update modul bulan desember
    x_service = fields.Selection(
                [('ass', 'KPB'), ('Lengkap', 'Service Lengkap'), ('LR', 'Light Repair'), ('GO', 'Ganti Oli '),
                 ('GOP', 'Ganti Oli Plus'), ('HR', 'Heavy Repair'), ('JR', 'Job Return'),
                 ('OJ', 'Other Job'), ('CL', 'Claim'),  ('SK', 'Service Kunjungan'), ('MP', 'Mutasi Cabang')], string="Service Type")


class SaleAddKendaraan(models.Model):
    _inherit = 'sale.order'

    unitPelanggan = fields.Many2one('simontir.unitpelanggan',string='Kendaraan')

    @api.onchange('unitPelanggan')
    def set_partner(self):
        if self.unitPelanggan and self.unitPelanggan.pelanggan:
            self.partner_id = self.unitPelanggan.pelanggan
        else:
            self.partner_id = False