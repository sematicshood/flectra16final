# -*- coding: utf-8 -*-

from flectra import models, fields, api


class simontir(models.Model):
     _name = 'simontir.simontir'

     nama           = fields.Char()
     test1          = fields.Integer()
     test2          = fields.Float(compute="_value_pc", store=True)
     description    = fields.Text()

     @api.depends('test2')
     def _value_pc(self):
         self.test2 = float(self.test1) / 100


class JenisKendaraan(models.Model):
    _name = 'simontir.jeniskendaraan'

    name = fields.Char()
    type = fields.Char(size=20)
    merk = fields.Char(size=20)
    kapmesin = fields.Integer()
    transmisi = fields.Selection(
                [('Man', 'Manual'), ('Mat', 'Matic')],
                string="Transmisi")
    company_id = fields.Many2one('res.company', 'Company')

class unitPelanggan(models.Model):
    _name = 'simontir.unitpelanggan'

    name = fields.Char(string='Nopol')

    nomesin = fields.Char(size=25)
    norangka = fields.Char(seze=25)
    tahunbuat = fields.Integer()
    jenisKendaraan = fields.Many2one('simontir.jeniskendaraan', string='Model Kendaraan')
    pelanggan = fields.Many2one('res.partner', string='Pelanggan')

