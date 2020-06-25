# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from flectra.exceptions import UserError
from addons.wa_automation.models.sender import Send_Whatsapp
from addons.wa_automation.models.worker import sender_task


class wa_automation(models.Model):
    _name = 'wa_automation.wa_automation'
    _description = 'Database for wa automation'

    # code_order = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    nama_konsumen = fields.Char('Nama Konsumen', required=True)
    no_wa = fields.Char('Nomor Whatsapp', required=True)
    tanggal_order = fields.Date('Tanggal Order', required=True)
    welcome = fields.Boolean('Selamat Datang', default=False)
    fu_1 = fields.Boolean('Follow Up 1', default=False)
    fu_2 = fields.Boolean('Follow Up 2', default=False)
    fu_3 = fields.Boolean('Follow Up 3', default=False)
    promo = fields.Boolean('Promo', default=False)
    order_detail = fields.Char('Keterangan Order')
    schedule = fields.Date('Jadwal WhatsApp', default='')
    bokeh_chart = fields.Text(string='Bokeh Chart',compute='_compute_bokeh_chart',)
    


class My_Dashboard(models.Model):
    _name = 'wa_automation.my_dashboard'
    _description = 'Dashboard for wa automation'

    filter_date_end = fields.Date('Start Date', default='')
    filter_date = fields.Date('End Date', default='')


class Sendwa(models.TransientModel):

    _name = 'wa_automation.wizards.sendwa'

    message_fu_1 = fields.Text('Follow Up 1')
    message_fu_2 = fields.Text('Follow Up 2')
    message_fu_3 = fields.Text('Follow Up 3')
    message_welcome = fields.Text('Selamat Datang')
    message_promo = fields.Text('Promo')
    send_type = fields.Selection(selection=[('follow_up_1', 'Follow Up 1'),
                ('follow_up_2', 'Follow Up 2'),('follow_up_3', 'Follow Up 3'),
                ('follow_up_welcome', 'Selamat Datang'), ('promo', 'Promo')],
                string='Tipe Kirim', default='') 

    @api.multi
    def confirm_button(self):
        message_fu_1 = self.message_fu_1
        message_fu_2 = self.message_fu_2
        message_fu_3 = self.message_fu_3
        message_welcome = self.message_welcome
        message_promo = self.message_promo
        send_type = self.send_type
        message = ""
        flag_type = ""

        if not send_type:
            raise UserError('Tipe kirim tidak boleh kosong!')

        if not message_fu_1 and not message_fu_2 and not message_fu_3 and not message_welcome and not message_promo:
            raise UserError('Message tidak boleh kosong!')

        if send_type == 'follow_up_1' and message_fu_1:
            flag_type = 'fu_1'
            message = message_fu_1
        elif send_type == 'follow_up_2' and message_fu_2:
            flag_type = 'fu_2'
            message = message_fu_2
        elif send_type == 'follow_up_3' and message_fu_3:
            flag_type = 'fu_3'
            message = message_fu_3
        elif send_type == 'follow_up_welcome' and message_welcome:
            flag_type = 'welcome'
            message = message_welcome
        elif send_type == 'promo' and message_promo:
            flag_type = 'promo'
            message = message_promo
    

        accounts_sended = self.env['wa_automation.wa_automation'].search(
                        [(flag_type,'=', False)])

        for account in accounts_sended:
            phone = account.no_wa
            if phone:
                if flag_type == 'fu_1':
                    account.fu_1 = True
                elif flag_type == 'fu_2':
                    account.fu_2 = True
                elif flag_type == 'fu_3':
                    account.fu_3 = True
                elif flag_type == 'welcome':
                    account.welcome = True
                elif flag_type == 'promo':
                    account.promo = True

                sender = Send_Whatsapp(phone, message)
                status = sender.send_post('chat', 'text')

class SendwaScheduled(models.TransientModel):

    _name = 'wa_automation.wizards.sendwaschaduled'

    message_scheduled = fields.Text('WhatsApp Terjadwal')
    no_wa = fields.Char('Nomor Whatsapp', default='')
    interval = fields.Selection([('6', '6 jam'), ('12', '12 jam'), ('24', '24 jam')], default='', string="Set Interval Waktu")

    @api.multi
    def confirm_button(self):
        message_scheduled = self.message_scheduled
        no_wa = self.no_wa
        interval = self.interval

        if not message_scheduled or not interval or not no_wa:
            raise UserError('Form belum lengkap!')

        sender_task(message_scheduled, interval, no_wa)