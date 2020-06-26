# -*- coding: utf-8 -*-

from flectra import models, fields, api
from addons.crmwa.crmwa.models.sendwa import Send_Whatsapp
from datetime import datetime, timedelta
from flectra.exceptions import UserError


class Accounts(models.Model):
    _name = 'cmrwa.accounts'
    
    nama_konsumen = fields.Char('Nama Konsumen', required=True)
    no_wa = fields.Char('Nomor Whatsapp', required=True)
    no_motor = fields.Char('Nomor Motor', required=True)
    tanggal_input = fields.Date('Tanggal Service Terakhir', required=True)
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
    terkirim = fields.Boolean('Terkirim', default=False)
    sendimage = fields.Boolean(default=False)


class Sendwa(models.TransientModel):

    _name = 'crmwa.wizards.sendwa'
    # _inherit = 'cmrwa.accounts'

    message_h7 = fields.Text('Message H7')
    message_h3 = fields.Text('Message H3')
    url_image = fields.Text("Url Image")
    # new_image = fields.Binary("Image", attachment=True,
    #     help="This field holds the image used as crmwa image, limited to 1024x1024px",)

    # new_website_url = fields.Char('Website URL', compute='_compute_website_url', store= True,
    #                  compute_sudo=True, help='The full URL to access the document through the website.')

    # @api.multi
    # def _compute_website_url(self):
    #     unique = self.env['ir.attachment'].search([('id','>', 1)])
    #     unique_one = self.env['ir.attachment'].search([('id','=',unique[0].id)])
    #     unique_one.public = True
    #     print("uni", unique_one.checksum, unique_one.website_url, unique_one.local_url, unique_one.url,
    #         unique_one.store_fname, unique_one.res_name, unique_one.res_model, unique_one.res_id, unique_one.res_field, unique_one.public, unique_one.name )       
    #     for record in self:
    #         print("res_id", unique_one.res_id)
    #         unique_again = self.env['ir.attachment'].search([('res_id','=', unique_one.res_id)])
    #         print("oke", unique_again)
    #         record.new_website_url = 'http://localhost:7073/web/image/{}?unique={}'.format(unique[0].id, unique_one.checksum)
    #         # record.website_url = 'localhost:7073/web/image?model=crmwa.wizards.sendwa&id={}&field=image'.format(record.id)

    @api.multi
    def confirm_button(self):
        current_date = datetime.today().strftime('%Y-%m-%d')
        message_h7 = self.message_h7
        message_h3 = self.message_h3
        url_image = self.url_image
        message = ""

        if not message_h7 and not message_h3 and not url_image:
            raise UserError('Message atau image tidak boleh kosong!')
        
        if message_h7:
            message = message_h7
        
        if message_h3:
            message = message_h3

        is_image = False
        if url_image and len(url_image) > 12:
            is_image = True
            

        accounth7 = self.env['cmrwa.accounts'].search([('tanggal_h7','=', current_date)])
        accounth3 = self.env['cmrwa.accounts'].search([('tanggal_h3','=', current_date)])
        accounttelpon = self.env['cmrwa.accounts'].search([('tanggal_telpon','=', current_date)])

        accounts = accounth7 + accounth3 + accounttelpon
        phones = []
        for account in accounts:
            phone = account.no_wa
            tanggal_h7 = account.tanggal_h7
            tanggal_h3 = account.tanggal_h3
            tanggal_telpon = account.tanggal_telpon
            status_kedatangan = account.status_kedatangan
            status_follow_up = account.status_follow_up
            terkirim = account.terkirim
            sendimage = account.sendimage

            if phone:
                if is_image and not sendimage:
                    sender = Send_Whatsapp(phone, url_image)
                    status = sender.send_image('media', 'url')
                    if status == 200:
                        account.sendimage = True
                        
                else: 
                    if (current_date == tanggal_h7) and not status_kedatangan and (status_follow_up != 'H-7' or (status_follow_up == 'H-7' and not terkirim)) and message_h7:
                        account.status_whatsapp = True
                        account.status_follow_up = 'H-7'
                        if not terkirim:
                            sender = Send_Whatsapp(phone, message)
                            status = sender.send_post('chat', 'text')

                        if status == 200:
                            account.terkirim = True

                    elif (current_date == tanggal_h3) and not status_kedatangan and (status_follow_up != 'H-3' or (status_follow_up == 'H-3' and not terkirim)) and message_h3:
                        account.status_whatsapp = True
                        account.status_follow_up = 'H-3'
                        if not terkirim:
                            sender = Send_Whatsapp(phone, message)
                            status = sender.send_post('chat', 'text')

                        if status == 200:
                            account.terkirim = True

                    elif (current_date == tanggal_telpon) and not status_kedatangan and (status_follow_up != 'Ditelpon' or (status_follow_up == 'Ditelpon' and not terkirim)):
                        account.status_whatsapp = True
                        account.status_follow_up = 'Ditelpon'
                        account.status_call = True
                        account.terkirim =  True


class Getkonsumen(models.TransientModel):

    _name = 'crmwa.wizards.getkonsumen'

    @api.multi
    def confirm_button2(self):
        batas = '2020-03-02 07:14:17'
        sales = self.env['sale.order'].search([('date_order','>', batas)])

        for sale in sales:
            check = self.env['cmrwa.accounts'].search([('no_motor','=', sale.access_token)], limit=1)
            no_motor = check.no_motor
            if no_motor:
                cr_date = datetime.strptime(sale.date_order, '%Y-%m-%d %H:%M:%S')
                if cr_date.strftime('%Y-%m-%d') != check.tanggal_input:
                    cr_date = datetime.strptime(sale.date_order, '%Y-%m-%d %H:%M:%S')
                    tanggal_h7 = cr_date + timedelta(days=53)
                    tanggal_h3 = cr_date + timedelta(days=57)
                    tanggal_telpon = cr_date + timedelta(days=59)
                    check.tanggal_input=  cr_date.strftime('%Y-%m-%d')
                    check.tanggal_h7 =tanggal_h7.strftime('%Y-%m-%d')
                    check.tanggal_h3 = tanggal_h3.strftime('%Y-%m-%d')
                    check.tanggal_telpon=  tanggal_telpon.strftime('%Y-%m-%d') 
                    check.status_whatsapp = False
                    check.status_kedatangan = False
                    check.status_follow_up = ""                    
         
            if not check.id:
                cr_date = datetime.strptime(sale.date_order, '%Y-%m-%d %H:%M:%S')
                tanggal_h7 = cr_date + timedelta(days=53)
                tanggal_h3 = cr_date + timedelta(days=57)
                tanggal_telpon = cr_date + timedelta(days=59)
                cek = self.env['res.partner'].search([('id', '=', sale.partner_id.id)])
                phone = cek.mobile
                if not phone:
                    phone = ""
                phone = str(phone)
                if len(phone) > 6:
                    data = {
                    "nama_konsumen": sale.name,
                    "no_wa": phone,
                    "no_motor": sale.access_token,
                    "tanggal_input": cr_date.strftime('%Y-%m-%d'),
                    "tanggal_h7": tanggal_h7.strftime('%Y-%m-%d'),
                    "tanggal_h3": tanggal_h3.strftime('%Y-%m-%d'),
                    "tanggal_telpon": tanggal_telpon.strftime('%Y-%m-%d') 
                    }
                    self.env['cmrwa.accounts'].create(data)
                # try:
                #     number = str(phone)
                #     is_valid = carrier._is_mobile(number_type(phonenumbers.parse(number)))
                # except:
                #     is_valid = False
                
                # if is_valid:
                #     data = {
                #     "nama_konsumen": sale.name,
                #     "no_wa": phone,
                #     "no_motor": sale.access_token,
                #     "tanggal_input": cr_date.strftime('%Y-%m-%d'),
                #     "tanggal_h7": tanggal_h7.strftime('%Y-%m-%d'),
                #     "tanggal_h3": tanggal_h3.strftime('%Y-%m-%d'),
                #     "tanggal_telpon": tanggal_telpon.strftime('%Y-%m-%d') 
                #     }
                #     self.env['cmrwa.accounts'].create(data)
