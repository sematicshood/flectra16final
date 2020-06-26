# -*- coding: utf-8 -*-

from flectra import models, fields, api
from datetime import datetime, timedelta
from flectra.exceptions import UserError


class marketing_chart(models.Model):
    _name = 'marketing_chart.marketing_chart'

    types = fields.Char(string="Type", default="")
    penjualan = fields.Char(string="Nama", default="")
    totalnya = fields.Char(string="Total", default="")


class Getkonsumen(models.TransientModel):

    _name = 'marketing_chart.wizards.getkonsumen'

    get_type = fields.Selection([
            ('produk', 'Produk'),
            ('category', 'Kategori'),
            ('salesman', 'Salesman'),
            ('konsumen', 'Konsumen'),
        ],)

    rangenya = fields.Selection([
            ('10', '10'),
            ('20', '20'),
            ('50', '50'),
        ],)    

    indikator = fields.Selection([
            ('tertinggi', 'Tertinggi'),
            ('terendah', 'Terendah'),
        ],)    

    @api.multi
    def confirm_button2(self):
        get_type = self.get_type
        rangenya = self.rangenya
        indikator = self.indikator

        if not get_type or not rangenya or not indikator:
            raise UserError('Lengkapi form get data!')

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cr_date = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        batas = cr_date - timedelta(days=30)
        sales = self.env['sale.order'].search([('date_order','>=', batas.strftime('%Y-%m-%d'))],limit=20)

        total_amount = []
        names = []
        datenya = []
        list_dict_prices = []

        for sale in sales:
            orders = sale.order_line
            if orders:
                for order in orders:
                    price_unit = order.price_unit
                    if get_type == 'produk':
                        main_get = sale.product_id.name
                    elif get_type == 'category':
                        main_get = sale.product_id.type
                    elif get_type == 'salesman':
                        main_get = sale.user_id.name
                    elif get_type == 'konsumen':
                        main_get = sale.partner_id.name
                    else:
                        raise UserError('Error pemilihan tipe!')

                    if main_get:
                        main_dict = {
                            str(main_get):int(price_unit)
                        }
                        list_dict_prices.append(main_dict)

        result = {} 
        for d in list_dict_prices: 
            for k in d.keys(): 
                result[k] = result.get(k, 0) + d[k]

        if indikator == 'tertinggi':
            sorted_dict = sorted(result.items(), key=lambda x: x[1], reverse=True)
        else:
             sorted_dict = sorted(result.items(), key=lambda x: x[1])      

        limit = 0
        for value in sorted_dict:
            if limit <= int(rangenya):
                data = {
                        "types":get_type,
                        "penjualan": value[0],
                        "totalnya": value[1]
                        }
                self.env['marketing_chart.marketing_chart'].create(data)
                limit+=1   

        # if indikator == 'tertiggi':
        #     list_sorted = sorted(list_dict_prices, key = lambda i: i['total'],reverse=True)
        # else:
        #     list_sorted = sorted(list_dict_prices, key = lambda i: i['total'])
        
        # print("cek", list_sorted)


        


        #     so_name = sale.name,
        #     produk = sale.product_id.name,
        #     category = sale.product_id.type,
        #     salesman = sale.user_id.name,
        #     konsumen = sale.partner_id.name,
        #     source = sale.source_id.name,
        #     total = sale.amount_total,
        #     tanggal_order = sale.date_order,
        #     token = sale.access_token
        #     name = sale.partner_id.name
        #     code = sale.name
        #     date = sale.date_order
        #     product_name = sale.product_id.name

        #     if not product_name:
        #         product_name = "Untitled"
        #     price_unit = sale.product_id.lst_price
        #     if not price_unit:
        #         price_unit = 0
        #     if date:
        #         datenya.append(str(date))
        #         dict_price = {str(product_name):int(price_unit)}
        #         list_dict_prices.append(dict_price)
        #         if not name:
        #             name = "No Name"
        #         name = name + " " + code
        #         names.append(name)

        #         amount = sale.amount_total
        #         if not amount:
        #             amount = 0
        #         total_amount.append(int(amount))

        # result = {} 
        # for d in list_dict_prices: 
        #     for k in d.keys(): 
        #         result[k] = result.get(k, 0) + d[k]

        # k, v = [], []
        # for a, b in result.items():
        #     k.append(a)
        #     v.append(b)        

        # dist_name = {k: v for k, v in zip(names, total_amount)}



        # for sale in sales:
        #     check = self.env['marketing_chart.marketing_chart'].search([('token','=', sale.access_token)], limit=1)
        #     if not check:
        #         orders = sale.order_line
        #         if orders:
        #             for order in orders:
        #                 data = {
        #                 "so_name": sale.name,
        #                 "produk": sale.product_id.name,
        #                 "category": sale.product_id.type,
        #                 "salesman":sale.user_id.name,
        #                 "konsumen":sale.partner_id.name,
        #                 "source":sale.source_id.name,
        #                 "total":order.price_unit,
        #                 "tanggal_order": sale.date_order,
        #                 "token": sale.access_token
        #                 }
        #                 self.env['marketing_chart.marketing_chart'].create(data)            
            # else:
            #     print("cek")
            #     data = {
            #     "so_name": sale.name,
            #     "produk": sale.product_id.name,
            #     "category": sale.product_id.type,
            #     "salesman":sale.user_id.name,
            #     "source":sale.source_id,
            #     "tanggal_order": sale.date_order 
            #     }
            #     self.env['marketing_chart.marketing_chart'].create(data)    