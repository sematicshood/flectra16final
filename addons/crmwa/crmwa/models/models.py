# -*- coding: utf-8 -*-

from flectra import models, fields, api
from addons.crmwa.crmwa.models.sendwa import Send_Whatsapp
from datetime import datetime, timedelta
from flectra.exceptions import except_orm


class Accounts(models.Model):
    _name = 'cmrwa.accounts'
    
    nama_konsumen = fields.Char('Nama Konsumen', required=True)
    no_wa = fields.Char('Nomor Whatsapp', required=True)
    no_motor = fields.Char('Nomor Motor', required=True)
    tanggal_input = fields.Date('Tanggal Input', required=True)
    tanggal_h7 = fields.Date('Tanggal H-7', required=True)
    tanggal_h3 = fields.Date('Tanggal H-3', required=True)
    tanggal_telpon = fields.Date('Tanggal Ditelpon', required=True)
    status_whatsapp = fields.Boolean('Sudah di WA', default=False)
    status_kedatangan = fields.Boolean('Sudah datang', default=False)
    status_follow_up = fields.Char('Status Follow Up')
    tipe_motor = fields.Char('Tipe Motor')
    km_akhir = fields.Char('Kilo Meter Akhir')
    ket = fields.Char('Alasan')
    status_call = fields.Boolean('Status Telpon', default=False)

class Sendwa(models.TransientModel):

    _name = 'crmwa.wizards.sendwa'
    # _inherit = 'cmrwa.accounts'

    message_h7 = fields.Char('Message H7')
    message_h3 = fields.Char('Message H3')

    @api.multi
    def confirm_button(self):
        current_date = datetime.today().strftime('%Y-%m-%d')
        message_h7 = self.message_h7
        message_h3 = self.message_h3
        message = ""

        if not message_h7 and not message_h3:
            raise except_orm('confirm_button','Message tidak boleh kosong!')
        
        if message_h7:
            message = message_h7
        
        if message_h3:
            message = message_h3
            
        accounts = self.env['cmrwa.accounts'].search([])
        phones = []
        for account in accounts:
            phone = account.no_wa
            tanggal_h7 = account.tanggal_h7
            tanggal_h3 = account.tanggal_h3
            tanggal_telpon = account.tanggal_telpon
            status_kedatangan = account.status_kedatangan
            status_follow_up = account.status_follow_up
            
            if phone:
                if (current_date == tanggal_h7) and not status_kedatangan and status_follow_up != 'H-7':
                    account.status_whatsapp = True
                    account.status_follow_up = 'H-7'
                    phones.append(phone)

                elif (current_date == tanggal_h3) and not status_kedatangan and status_follow_up != 'H-3':
                    account.status_whatsapp = True
                    account.status_follow_up = 'H-3'
                    phones.append(phone)
                
                elif (current_date == tanggal_telpon) and not status_kedatangan and status_follow_up != 'Ditelpon':
                    account.status_whatsapp = True
                    account.status_follow_up = 'Ditelpon'
                    account.status_call = True

        if phones:
            sender = Send_Whatsapp(phones, message)
            status = sender.send_post('chat', 'text')
            if status == 'gagal':
                raise except_orm('confirm_button','Service whatsapp error, coba restart whatsapp web lagi')


class Getkonsumen(models.TransientModel):

    _name = 'crmwa.wizards.getkonsumen'

    @api.multi
    def confirm_button2(self):
        sales = self.env['sale.order'].search([], limit=10)
        for sale in sales:
            cr_date = datetime.strptime(sale.write_date, '%Y-%m-%d %H:%M:%S')
            tanggal_h3 = cr_date + timedelta(days=4)
            tanggal_telpon = cr_date + timedelta(days=6)
            data = {
            "nama_konsumen": sale.name,
            "no_wa": sale.access_token,
            "no_motor": sale.access_token,
            "tanggal_input": cr_date.strftime('%Y-%m-%d'),
            "tanggal_h7": cr_date.strftime('%Y-%m-%d'),
            "tanggal_h3": tanggal_h3.strftime('%Y-%m-%d'),
            "tanggal_telpon": tanggal_telpon.strftime('%Y-%m-%d') 
            }
            self.env['cmrwa.accounts'].create(data)
