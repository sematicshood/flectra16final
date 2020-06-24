# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra import exceptions
import uuid
from datetime import datetime
from flectra.exceptions import UserError
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import row
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import PuBu
from bokeh.models import ColumnDataSource, ranges, LabelSet, HoverTool
from math import pi
import pandas as pd
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter

# class dashboard_marketing(models.Model):
#     _name = 'dashboard_marketing.dashboard_marketing'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class my_dashboard(models.Model):
    _name = 'dashboard_marketing.my_dashboard'
    _description = 'Dashboard for wa automation'

    filter_date_end = fields.Date('Start Date', default='')
    filter_date = fields.Date('Until Date', default='')

    bokeh_chart = fields.Text(string='Bokeh Chart',compute='_compute_bokeh_chart', defaul='')

    def _compute_bokeh_chart(self):
        if not self.filter_date and self.filter_date_end:
            raise UserError("Filter date harus diisikan semua.")

        sales = self.env['sale.order'].search([('date_order', '<=', self.filter_date),
                                                ('date_order', '>=', self.filter_date_end)],
                                                limit=50)

        valid_sales = len(sales)
        if valid_sales == 0:
            raise UserError("Tidak ada penjualan pada range tanggal tersebut.")

        total_amount = []
        names = []
        datenya = []
        list_dict_prices = []
        for sale in sales:
            name = sale.partner_id.name
            code = sale.name
            date = sale.date_order
            product_name = sale.product_id.name
            if not product_name:
                product_name = "Untitled"
            price_unit = sale.product_id.lst_price
            if not price_unit:
                price_unit = 0
            if date:
                datenya.append(str(date))
                dict_price = {str(product_name):int(price_unit)}
                list_dict_prices.append(dict_price)
                if not name:
                    name = "No Name"
                name = name + " " + code
                names.append(name)

                amount = sale.amount_total
                if not amount:
                    amount = 0
                total_amount.append(int(amount))

        result = {} 
        for d in list_dict_prices: 
            for k in d.keys(): 
                result[k] = result.get(k, 0) + d[k]

        k, v = [], []
        for a, b in result.items():
            k.append(a)
            v.append(b)        

        dist_name = {k: v for k, v in zip(names, total_amount)}
        start, end = str(self.filter_date_end), str(self.filter_date_end)
        title_graph = "Grafik Penjualan Dari Tanggal {} - Tanggal {}".format(start, end)
        highest_title_graph = "Grafik Penjualan Tertinggi Dari Tanggal {} - Tanggal {}".format(start, end)
        for rec in self:

            source = ColumnDataSource(data=dict(
                x=names,
                y=total_amount,
                desc=datenya,
            ))

            TOOLTIPS = [
                ("indeks", "$index"),
                ("desc", "@desc"),
            ]

            #PIE
            # x = dist_name
            # data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
            # data['angle'] = data['value']/data['value'].sum() * 2*pi
            # data['color'] = Category20c[len(x)]

            # p3 = figure(plot_width=800, plot_height=500, title=title_graph, toolbar_location=None,
            #         tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

            # p3.wedge(x=0, y=1, radius=0.4,
            #         start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            #         line_color="white", fill_color='color', legend='country', source=data)

            # p3.axis.axis_label=None
            # p3.axis.visible=False
            # p3.grid.grid_line_color = None
            # p3.xaxis.major_label_orientation = 1.2
            # tab3 = Panel(child=p3, title="Pie")

            #BAR
            p = figure(x_range=names, plot_width=800, plot_height=500, title=title_graph, tooltips=TOOLTIPS)
            p.vbar(x=names, width=0.5, bottom=0,top=total_amount, color="firebrick")
            p.xgrid.grid_line_color = None
            p.y_range.start = 0
            p.xaxis.major_label_orientation = 1.2
            tab0 = Panel(child=p, title="bar")

            #CICLE
            p1 = figure(x_range=names, plot_width=800, plot_height=500, title=title_graph,
                    toolbar_location=None, tooltips=TOOLTIPS)
            p1.circle('x', 'y', size=20, color="navy", alpha=0.5, source=source)
            p1.xgrid.grid_line_color = None
            p1.y_range.start = 0
            p1.xaxis.major_label_orientation = 1.2
            tab1 = Panel(child=p1, title="circle")

            #LINE
            p2 = figure(x_range=names, plot_width=800, plot_height=500, title=title_graph,
                    toolbar_location=None)
            p2.line(names, total_amount, line_width=3, color="navy", alpha=0.5)
            p2.xgrid.grid_line_color = None
            p2.y_range.start = 0
            p2.xaxis.major_label_orientation = 1.2
            tab2 = Panel(child=p2, title="line")

            #BAR
            p4 = figure(x_range=k, plot_width=800, plot_height=500, title=highest_title_graph)
            p4.vbar(x=k, width=0.5, top=v, color="firebrick")
            p4.xgrid.grid_line_color = None
            p4.y_range.start = 0
            p4.xaxis.major_label_orientation = 1.2
            tab4 = Panel(child=p4, title="bar")

            tabs = Tabs(tabs=[ tab1, tab2, tab0, tab4 ])

            script, div = components(tabs)
            tes = '%s%s\n\n\n' % (div, script)

            
            rec.bokeh_chart = tes 