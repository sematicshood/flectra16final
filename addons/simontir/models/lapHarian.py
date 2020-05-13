from flectra import models, fields, api
import datetime
from datetime import datetime, timedelta


class LapHarian(models.Model):
    _name = 'simontir.lapharian'

    tglLap = fields.Date()
    omsetJasa = fields.Float()
    omsetKpbOli = fields.Float()
    omsetKpb = fields.Float()
    omsetTotalJasa = fields.Float()
    omsetPart = fields.Float()
    omsetPartOli = fields.Float()
    omsetPartBusi = fields.Float()
    omsetTotalPart = fields.Float()
    omsetPos = fields.Float()
    omsetgrandtotal = fields.Float()
    biayaHarian = fields.Float()
    labaharian = fields.Float()
    printLap = fields.Text()
    kasir = fields.Many2one('res.users', string='Kasir')
    totalAss1 = fields.Integer()
    totalAss2 = fields.Integer()
    totalAss3 = fields.Integer()
    totalAss4 = fields.Integer()
    totalGo = fields.Integer()  # x_ganti_oli
    totalHr = fields.Integer()  # x_turun_mesin
    totalQs = fields.Integer()  # x_antrian_service Pit express
    totalBs = fields.Integer()  # x_antrian_service Booking service
    totalreg = fields.Integer()  # x_antrian_service Reguler
    totalft = fields.Integer()  # fast track
    totalpit = fields.Integer()  # fast track
    totalGop = fields.Integer()  # x_ganti_part
    totalSl = fields.Integer()  # x_service lengkap
    totalSr = fields.Integer()  # x_service ringan
    totalClaim = fields.Integer()  # x_claim
    totalJr = fields.Integer()  # x_job_return
    totalSk = fields.Integer()  # service kunjungan
    totalOj = fields.Integer()  # other job
    totalSp = fields.Integer()  # spesial program
    totalCuci = fields.Integer()  # x_is_wash
    selisih = fields.Float()
    totalCash = fields.Float()
    totalEdc = fields.Float()
    totalue = fields.Integer()
    totalpopart = fields.Float()
    totalkasin = fields.Float()
    totalkas = fields.Float()
    totalbank = fields.Float()
    totalbiaya = fields.Float()
    catatan = fields.Text()
    totalkasnet = fields.Float()
    totalpospart = fields.Float()
    totalposoli = fields.Float()
    totalposbusi = fields.Float()
    totalblmlunas = fields.Float()
    totalinbatal = fields.Float()
    totaloutbatal = fields.Float()
    listinvblmlunas = fields.Text()
    listedc = fields.Text()
    listbiayaharian = fields.Text()
    listbelipart = fields.Text()
    lateinv = fields.Text()
    notpaidinv = fields.Text()
    saldoawal = fields.Float(string='Saldo Awal')
    setoranbank = fields.Float(string='Setoran Bank')
    uangkashrini = fields.Float()
    fisikuang = fields.Float(string='Fisik Uang Kas')
    saldoakhirhrini = fields.Float()
    totalcr = fields.Integer()
    company = fields.Many2one('res.company', string='Perusahaan')
    totalbsmtd = fields.Integer(string='BS MTD')
    totaluemtd = fields.Integer(string='UE MTD')

    def getIdProduct(self, category):
        product = self.env['product.product'].sudo()

        return [p.id for p in product.search([
            ('categ_id', 'ilike', category)
        ])]

    @api.multi
    def generateLaporanHarian(self):
        da = datetime.strptime(self.tglLap, '%Y-%m-%d')
        d1 = datetime.strftime(da, "%Y-%m-%d 00:00:00")
        d2 = datetime.strftime(da, "%Y-%m-%d 23:59:59")
        bulan = int(da.strftime("%m"))
        tahun = int(da.strftime("%Y"))
        if bulan == 1:
            bln = 12
            thn = tahun - 1
        else:
            bln = int(da.strftime("%m")) - 1
            thn = int(da.strftime("%Y"))
        nda = datetime(int(thn), int(bln), 29)
        nd1 = datetime.strftime(nda, '%Y-%m-%d 00:00:00')
        # update by denny tgl 14 des
        # deskripsi : update utk tampilkan invoice belum bayar
        list_notpaidinv = ''
        x_invblmlunas = 0
        bstotmtd = self.env['sale.order'].sudo().search_count([('date_order', '>=', nd1),
                                                               ('date_order', '<', d2), ('state', '=', 'done'),
                                                               ('x_antrian_service', '=', 'BS'),
                                                               ('company_id', '=', self.company.id)])
        uetotmtd = self.env['sale.order'].sudo().search_count([('date_order', '>=', nd1),
                                                               ('date_order', '<', d2), ('state', '=', 'done'),
                                                               ('company_id', '=', self.company.id)])

        xxx = self.company.id
        so = self.env['sale.order'].sudo().search([('date_order', '>=', d1),
                                                   ('date_order', '<', d2), ('state', '=', 'done'),
                                                   ('x_antrian_service', '<>', 'MP'),
                                                   ('company_id', '=', self.company.id)])
        # inv = self.env['account.invoice.line'].sudo().search([('create_date', '>=', d1),
        # ('create_date', '<', d2), ('sale_line_ids', '=', True)])
        inv = self.env['account.invoice'].sudo().search([('date_invoice', '=', da),
                                                         ('state', 'in', ['open', 'paid', 'draft']),
                                                         ('type', '=', 'out_invoice'),
                                                         ('company_id', '=', self.company.id)])
        # product = self.env['product.product'].sudo()
        # product_service = [p.id for p in product.search([
        #    ('type', '=', 'service')]
        # )]
        # update by denny tgl 14 des
        # deskripsi : update utk tampilkan invoice belum bayar
        piutang = self.env['account.invoice'].sudo().search([('date_invoice', '<', da),
                                                             ('state', 'in', ['open', 'draft']),
                                                             ('type', '=', 'out_invoice'),
                                                             ('company_id', '=', self.company.id)])

        x_omsetjasa = 0
        x_omsetglobal = 0
        x_omsetpart = 0
        x_omsetpartoli = 0
        x_omsetpartbusi = 0
        x_omsetkpb_oli = 0

        x_biayaharian = 0
        x_posbusi = 0
        x_pospart = 0
        x_posoli = 0
        x_posjasa = 0
        ass_1 = 0
        ass_2 = 0
        ass_3 = 0
        ass_4 = 0
        x_totalgo = 0
        x_bs = 0
        x_reguler = 0
        x_ft = 0
        x_pit = 0
        x_heavy_r = 0
        x_service_ringan = 0
        x_pos = 0
        x_cuci = 0
        x_sl = 0
        x_jr = 0
        x_claim = 0
        x_qs = 0
        x_sp = 0
        x_sk = 0
        x_oj = 0
        x_totalgp = 0
        x_totalue = 0
        x_totalpopart = 0
        x_totalinbound = 0
        x_kasmp = 0
        x_mandiri = 0

        x_omsetkpb = 0
        x_inrefund = 0
        x_outrefund = 0
        x_listbiayaharian = ''
        x_listedc = ''
        x_listbelipart = ''
        x_catatan = ''
        x_lateinv = ''

        x_saldoawal = 0
        x_setoranbank = 0
        x_uangkashrini = 0
        x_fisikuang = 0
        x_saldoakhirhrini = 0
        x_cr = 0

        x_partall = 0
        x_subtotal_edc = 0
        for sol in so:
            xsodd = sol.name
            # ASS I - IV => ass
            if sol.x_kpb == 1:
                ass_1 += 1
            elif sol.x_kpb == 2:
                ass_2 += 1
            elif sol.x_kpb == 3:
                ass_3 += 1
            elif sol.x_kpb == 4:
                ass_4 += 1
            # Kriteria HR + GO + GP => HR
            else:
                if sol.x_service == 'Lengkap':
                    x_sl += 1
                elif sol.x_service == 'LR':
                    x_service_ringan += 1
                elif sol.x_service == 'GO':
                    x_totalgo += 1
                elif sol.x_service == 'GOP':
                    x_qs += 1
                elif sol.x_service == 'HR':
                    x_heavy_r += 1
                elif sol.x_service == 'JR':
                    x_jr += 1
                elif sol.x_service == 'SK':
                    x_sk += 1
                elif sol.x_service == 'CL':
                    x_claim += 1
                elif sol.x_service == 'OJ':
                    x_oj += 1
                elif sol.x_service == 'SP':
                    x_sp += 1
                else:
                    x_oj += 1

            if sol.x_antrian_service == 'BS':
                x_bs += 1
            elif sol.x_antrian_service == 'FT':
                x_ft += 1
            elif sol.x_antrian_service == 'Pit':
                x_pit += 1
            else:
                x_reguler += 1

        x_totalue = ass_1 + ass_2 + ass_3 + ass_4 + x_heavy_r + x_sl + x_qs + x_totalgo + x_jr + x_claim + x_sk \
                    + x_sp + x_oj + x_service_ringan

        # TODO validasi status invoice lunas
        # TODO validasi KPB khusus
        for invl in inv:  # looping invoice nya
            # print(invl.name)

            if invl.state == 'paid':
                nosonya = invl.number  # ambil no invoice nya
                sonya = self.env['sale.order'].sudo().search(
                    [('name', '=', invl.origin), ('company_id', '=', self.company.id), ('x_antrian_service', '<>', 'MP'),])  # buat ambil data sales order
                issokpb = sonya.x_kpb  # cek KPB nya
                lineinv = self.env['account.invoice.line'].sudo().search([('invoice_id', '=', invl.number),
                                                                          ('company_id', '=',
                                                                           self.company.id)])  # get data invoice line
                # catatan buat cek invoice dan jumlahnya

                for inline in lineinv:  # looping dalam invoice utk ambil nilainya
                    id_product = inline.product_id
                    typeprod = id_product.type
                    categprod = id_product.categ_id.name
                    prodkpb = id_product.x_is_kpb
                    if typeprod == 'service':  # validasi tipe produk yg jasa / service
                        # self.omsetJasa += inline.price_total
                        if issokpb:
                            if prodkpb == 'KPB':  # validasi tipe produk yg jasa / service utk oli khusus kpb
                                x_omsetkpb += inline.price_unit
                        elif id_product.x_dept == 'CR':
                            x_cr += inline.price_total
                        else:
                            x_omsetjasa += inline.price_total
                    else:  # validasi tipe produk yg stockable/sparepart
                        if categprod == 'Ahmpart':
                            # self.omsetPart += inline.price_total
                            x_omsetpart += inline.price_total
                        elif categprod == 'Oli':  # validasi tipe part yg kategori oli
                            if issokpb == 1:
                                if prodkpb == 'KPB':  # validasi tipe produk yg jasa / service utk oli khusus kpb
                                    # self.omsetKpbOli += inline.price_total
                                    x_omsetkpb_oli += float(id_product.standard_price * inline.quantity)
                            else:
                                # self.omsetPartOli += inline.price_total
                                x_omsetpartoli += inline.price_total
                        elif categprod == 'Busi':  # validasi tipe part yg kategori busi
                            # self.omsetPartBusi += inline.price_total
                            x_omsetpartbusi += inline.price_total
                        else:
                            x_partall += inline.price_total
            else:
                list_notpaidinv += str(invl.date_invoice).ljust(15) + str(invl.partner_id.name).ljust(30) + str(
                    invl.nopol).ljust(15) + str(invl.number).ljust(15) + str(invl.amount_total).ljust(15) + '\n'
                x_invblmlunas += invl.amount_total

        x_omsetglobal = x_omsetpartbusi + x_omsetpartoli + x_omsetkpb_oli + x_omsetpart + x_omsetjasa

        # Section data POS
        poshead = self.env['pos.order'].sudo().search([('date_order', '>=', d1),  # buat ambil data POS HEAD
                                                       ('date_order', '<', d2), ('state', '=', 'done'),
                                                       ('company_id', '=', self.company.id)])

        for phead in poshead:
            xline = phead.lines
            for zline in xline:

                id_product = zline.product_id
                typeprod = id_product.type
                categprod = id_product.categ_id.name
                if typeprod == 'service':  # validasi tipe produk yg jasa / service
                    # self.omsetJasa += inline.price_total
                    x_posjasa += zline.price_subtotal
                else:  # validasi tipe produk yg stockable/sparepart
                    if categprod == 'Ahmpart':
                        # self.omsetPart += inline.price_total
                        x_pospart += zline.price_subtotal
                    if categprod == 'Oli':  # validasi tipe part yg kategori oli
                        x_posoli += zline.price_subtotal
                    if categprod == 'Busi':  # validasi tipe part yg kategori busi
                        # self.omsetPartBusi += inline.price_total
                        x_posbusi += zline.price_subtotal
        # Pembatalan invoice payment + pembatalan out dan in
        invbatal = self.env['account.invoice'].sudo().search([('date_invoice', '=', da),
                                                              ('state', 'in', ['paid']),
                                                              ('type', 'in', ['in_refund', 'out_refund']),
                                                              ('company_id', '=', self.company.id)])
        for batalin in invbatal:  # looping dalam expense utk ambil nilainya
            if batalin.type == 'in_refund':
                x_inrefund += batalin.amount_total
            else:
                x_outrefund += batalin.amount_total
        # Section data biaya harian
        expenseline = self.env['hr.expense.sheet'].sudo().search(
            [('accounting_date', '=', self.tglLap),  # buat ambil data expense hr
             ('state', '=', 'done'), ('company_id', '=', self.company.id)])
        for el in expenseline:  # looping dalam expense utk ambil nilainya
            x_biayaharian += el.total_amount
            x_listbiayaharian += el.name.ljust(40) + str('{:4,.0f}'.format(el.total_amount)).rjust(12) + '\n'

        expensepart = self.env['account.payment'].sudo().search([('payment_date', '=', self.tglLap),
                                                                 ('state', 'in', ['posted', 'reconciled']),
                                                                 ('company_id', '=', self.company.id)])

        for elp in expensepart:  # looping dalam expense utk ambil nilainya
            if elp.payment_type == 'outbound':
                respartner = elp.partner_id
                respartnerpayterm = respartner.property_supplier_payment_term_id
                if respartner.name:
                    # update by denny tgl 14 des
                    # deskripsi : update utk pembelian part yang kontan
                    if respartner.supplier:
                        if respartnerpayterm.name == 'Kontan':
                            x_totalpopart += elp.amount
                            x_listbelipart += respartner.name.ljust(40) + str('{:4,.0f}'.format(elp.amount)).rjust(
                                12) + '\n'
            else:
                if elp.payment_type == 'inbound':
                    if elp.journal_id.name == 'Bank Mandiri':
                        lateinv = self.env['account.invoice'].sudo().search([('number', '=', elp.communication),
                                                                             ('company_id', '=', self.company.id)])
                        # invoicedate = lateinv.date_invoice
                        x_mandiri += elp.amount
                        # if lateinv.date_invoice:
                        for ltinv in lateinv:
                            if elp.payment_date > ltinv.date_invoice:
                                x_lateinv += ltinv.date_invoice.ljust(10) + ' ' + (
                                    ltinv.nopol.ljust(10) if ltinv.nopol else '-') + ' ' + ltinv.number.ljust(
                                    15) + ' ' + str('{:4,.0f}'.format(elp.amount)).rjust(12) + '\n'
                        x_listedc += ltinv.number.ljust(15) + '' + (
                            ltinv.nomorkartu.ljust(20) if ltinv.nomorkartu else '-') + (
                                         ltinv.nmbank.ljust(20) if ltinv.nmbank else '-') + str(
                            '{:4,.0f}'.format(elp.amount)).rjust(12) + '\n'
                        x_subtotal_edc += elp.amount
                    elif elp.journal_id.name == 'Kas MP':
                        x_kasmp += elp.amount
                        lateinv = self.env['account.invoice'].sudo().search([('number', '=', elp.communication),
                                                                             ('company_id', '=', self.company.id)])
                        # invoicedate = lateinv.date_invoice
                        # if lateinv.date_invoice:
                        for ltinv in lateinv:
                            if elp.payment_date > ltinv.date_invoice:
                                x_lateinv += ltinv.date_invoice.ljust(10) + ' ' + (
                                    ltinv.nopol.ljust(10) if ltinv.nopol else '-') + ' ' + ltinv.number.ljust(
                                    15) + ' ' + str('{:4,.0f}'.format(elp.amount)).rjust(12) + '\n'
                            # x_lateinv += elp.name.ljust(40) + str('{:4,.0f}'.format(elp.amount)).rjust(12) + '\n'

        # update by denny tgl 14 des
        # deskripsi : update utk tampilkan invoice belum bayar (piutang)
        for lp in piutang:
            list_notpaidinv += str(lp.date_invoice).ljust(15) + str(lp.partner_id.name).ljust(30) + str(lp.nopol).ljust(
                15) + str(lp.number).ljust(15) + str(lp.amount_total).ljust(15) + '\n'
            x_invblmlunas += lp.amount_total

        x_totalinbound = x_kasmp + x_mandiri
        self.totalkas = x_kasmp
        self.totalbank = x_mandiri
        self.totalcr = x_cr
        self.omsetJasa = x_omsetjasa
        self.omsetPart = x_omsetpart
        self.omsetKpbOli = x_omsetkpb_oli
        self.omsetKpb = x_omsetkpb
        self.omsetPartBusi = x_omsetpartbusi
        self.omsetPartOli = x_omsetpartoli
        self.omsetPos = x_posbusi + x_posjasa + x_posoli + x_pospart
        self.omsetTotalJasa = float(self.omsetJasa) + float(self.omsetKpb) + float(self.totalcr)
        self.omsetTotalPart = self.omsetPartBusi + self.omsetPartOli + self.omsetPart + x_omsetkpb_oli + x_partall
        self.omsetgrandtotal = self.omsetPos + self.omsetTotalPart + self.omsetTotalJasa
        self.biayaHarian = x_biayaharian
        self.totalpopart = x_totalpopart
        self.labaharian = self.omsetgrandtotal - (self.biayaHarian + self.totalpopart)
        self.totalbiaya = float(self.totalpopart + self.biayaHarian)
        self.totalAss1 = ass_1
        self.totalAss2 = ass_2
        self.totalAss3 = ass_3
        self.totalAss4 = ass_4
        self.totalBs = x_bs
        self.totalreg = x_reguler
        self.totalpit = x_pit
        self.totalft = x_ft
        self.totalQs = x_qs
        self.totalGop = x_totalgp
        self.totalGo = x_totalgo
        self.totalSl = x_sl
        self.totalSr = x_service_ringan
        self.totalHr = x_heavy_r
        self.totalClaim = x_claim
        self.totalJr = x_jr
        self.totalCuci = x_cuci
        self.totalue = x_totalue
        self.totalkasin = x_totalinbound - x_inrefund - x_outrefund
        self.totalkasnet = (x_kasmp + self.omsetPos) - (self.totalbiaya)
        self.totalpospart = x_pospart
        self.totalposoli = x_posoli
        self.totalposbusi = x_posbusi
        self.totalblmlunas = x_invblmlunas
        self.listbiayaharian = x_listbiayaharian
        self.listbelipart = x_listbelipart
        self.listedc = x_listedc
        self.catatan = x_catatan
        self.lateinv = x_lateinv
        self.notpaidinv = list_notpaidinv
        self.totalbsmtd = bstotmtd
        self.totaluemtd = uetotmtd
        # ---hitungan saldo akhir
        self.uangkashrini = self.totalkasnet + self.saldoawal
        self.saldoakhirhrini = self.uangkashrini - self.setoranbank
        self.selisih = self.fisikuang - self.saldoakhirhrini
        # self.printLap = ' '
        tpl = self.env['mail.template'].search(
            [('name', '=', 'Laporan Harian Bengkel')])
        data = tpl.render_template(
            tpl.body_html, 'simontir.lapharian', self.id, post_process=False)
        self.printLap = data

    @api.multi
    def rekapproduktifitas(self):
        # get data karyawan from hr.employee self.env.user.company_id

        karyawan = self.env['hr.employee'].sudo().search([('company_id', '=', self.env.user.company_id.name),
                                                          ('job_id', 'in',
                                                           ['ass mekanik', 'Staff', 'front desk', 'Mekanik', 'mekanik',
                                                            'kepala mekanik', 'Kepala Mekanik', 'Final Check','Kasir',
                                                            'Service Advisor', 'Kepala Bengkel', 'kepala bengkel', 'PART COUNTER']),
                                                            ('active', '=', 'True')])
        dx = datetime.strptime(self.tglLap, '%Y-%m-%d')
        dy = datetime.strftime(dx, "%Y-%m-%d 00:00:00")
        dz = datetime.strftime(dx, "%Y-%m-%d 23:59:59")

        for lkar in karyawan:
            # ambil data sale order dengan filter (tgl, nama karyawan, status = done)
            xjabatan = lkar.job_id

            if xjabatan.name == 'Mekanik' or xjabatan.name == 'mekanik' or xjabatan.name == 'ass mekanik' or xjabatan.name == 'Final Check' \
                    or xjabatan.name == 'kepala mekanik' or xjabatan.name == 'Kepala Mekanik' or xjabatan.name == 'Service Advisor'\
                    or xjabatan.name == 'Kepala Bengkel' or xjabatan.name == 'kepala bengkel':
                somekanik = self.env['sale.order'].sudo().search([('date_order', '>=', dy),
                                                                  ('date_order', '<', dz),
                                                                  ('state', '=', 'done'),
                                                                  ('company_id', '=', self.env.user.company_id.name),
                                                                  ('mekanik_id', '=', lkar.name)])
                x_work = 'Mekanik'
                if somekanik.exists():
                    self.pushdata(somekanik, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Service Advisor' or xjabatan.name == 'mekanik' or xjabatan.name == 'Mekanik' or xjabatan.name == 'ass mekanik' \
                    or xjabatan.name == 'Final Check' or xjabatan.name == 'kepala mekanik' \
                    or xjabatan.name == 'Kepala Mekanik' or xjabatan.name == 'Staff' or xjabatan.name == 'front desk' \
                    or xjabatan.name == 'Kepala Bengkel' or xjabatan.name == 'kepala bengkel' or xjabatan.name == 'PART COUNTER':
                soseadv = self.env['sale.order'].sudo().search([('x_user_sa', '=', lkar.name),
                                                                ('date_order', '>=', dy),
                                                                ('date_order', '<', dz),
                                                                ('state', '=', 'done'),
                                                                ('company_id', '=', self.env.user.company_id.name)])
                x_work = 'Service Advisor'
                if soseadv.exists():
                    self.pushdata(soseadv, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Staff' or xjabatan.name == 'front desk' or xjabatan.name == 'Kepala Bengkel' \
                    or xjabatan.name == 'kepala bengkel' or xjabatan.name == 'PART COUNTER':
                sostaff = self.env['sale.order'].sudo().search([('user_id', '=', lkar.name),
                                                                ('date_order', '>=', dy),
                                                                ('date_order', '<', dz),
                                                                ('state', '=', 'done'),
                                                                ('company_id', '=', self.env.user.company_id.name)])
                x_work = 'Admin'
                if sostaff.exists():
                    self.pushdata(sostaff, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Final Check' or xjabatan.name == 'Mekanik' or xjabatan.name == 'mekanik' \
                    or xjabatan.name == 'kepala mekanik' or xjabatan.name == 'Kepala Mekanik' \
                    or xjabatan.name == 'Service Advisor' or xjabatan.name == 'kepala bengkel' or xjabatan.name == 'PART COUNTER':
                soseadv = self.env['sale.order'].sudo().search([('checker_id', '=', lkar.name),
                                                                ('date_order', '>=', dy),
                                                                ('date_order', '<', dz),
                                                                ('state', '=', 'done'),
                                                                ('company_id', '=', self.env.user.company_id.name)])
                x_work = 'Final Check'
                if soseadv.exists():
                    self.pushdata(soseadv, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Mekanik' or xjabatan.name == 'mekanik' or xjabatan.name == 'ass mekanik' or xjabatan.name == 'Final Check' \
                    or xjabatan.name == 'kepala mekanik' or xjabatan.name == 'Kepala Mekanik' or xjabatan.name == 'Service Advisor':
                socuci = self.env['sale.order'].sudo().search([('date_order', '>=', dy),
                                                                  ('date_order', '<', dz),
                                                                  ('state', '=', 'done'),
                                                                  ('company_id', '=', self.env.user.company_id.name),
                                                                  ('x_user_cuci', '=', lkar.name)])
                x_work = 'Cuci'
                if socuci.exists():
                    self.pushdata(socuci, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Staff' or xjabatan.name == 'front desk' or xjabatan.name == 'kasir' or xjabatan.name == 'PART COUNTER':
                sokasir = self.env['sale.order'].sudo().search([('x_kasir', '=', lkar.name),
                                                                ('date_order', '>=', dy),
                                                                ('date_order', '<', dz),
                                                                ('state', '=', 'done'),
                                                                ('company_id', '=', self.env.user.company_id.name)])
                x_work = 'Kasir'
                if sokasir.exists():
                    self.pushdata(sokasir, lkar.name, xjabatan.name, self.tglLap, x_work)
            if xjabatan.name == 'Staff' or xjabatan.name == 'Partman' or xjabatan.name == 'PART COUNTER':
                sopartman = self.env['sale.order'].sudo().search([('x_partman', '=', lkar.name),
                                                                ('date_order', '>=', dy),
                                                                ('date_order', '<', dz),
                                                                ('state', '=', 'done'),
                                                                ('company_id', '=', self.env.user.company_id.name)])
                x_work = 'Partman'
                if sopartman.exists():
                    self.pushdata(sopartman, lkar.name, xjabatan.name, self.tglLap, x_work)

    def pushdata(self, rsnya, v_name, v_dept, v_tgllap, v_work):
        x_omsetkpb = 0
        x_omsetkpboli = 0
        x_cr = 0
        x_omsetjasa = 0
        x_omsetpart = 0
        x_omsetpartoli = 0
        x_omsetpartbusi = 0
        ass_1 = 0
        ass_2 = 0
        ass_3 = 0
        ass_4 = 0
        x_heavy_r = 0
        x_sl = 0
        x_qs = 0
        x_totalgo = 0
        x_reguler = 0
        x_jr = 0
        x_claim = 0
        x_bs = 0
        x_totalue = 0
        x_partall = 0
        x_cucian = 0
        x_dept = ''
        x_work = ''
        xnamacuci = ''
        x_service_ringan = 0
        x_sk = 0
        x_sp = 0
        x_oj = 0
        x_ft = 0
        x_pit = 0
        x_jasahr = 0
        x_jmlcr = 0
        # xjabatan = self.job_id
        ishr = False
        if rsnya:
            for sl in rsnya:
                issokpb = sl.x_kpb  # cek KPB nya
                if sl.x_service == 'HR' and v_work == 'Mekanik':
                    ishr = True
                else:
                    ishr = False

                # sl.name
                # sl.mekanik_id.name
                invna = self.env['account.invoice'].sudo().search([('origin', '=', sl.name),
                                                                   ('company_id', '=', self.env.user.company_id.name),
                                                                   ])  # get data invoice line

                for tln in invna:
                    invno = tln.number
                    lineinv = self.env['account.invoice.line'].sudo().search([('invoice_id', '=', invno),
                                                                              ('company_id', '=',
                                                                               self.env.user.company_id.name)])  # get data invoice line
                    # Data collecting for unit entri
                    # xsodd = sl.name
                    # ASS I - IV => ass
                    for ln in lineinv:
                        # ambil nilai jasanya

                        id_product = ln.product_id
                        typeprod = id_product.type
                        categprod = id_product.categ_id.name
                        prodkpb = id_product.x_is_kpb
                        if typeprod == 'service':  # validasi tipe produk yg jasa / service
                            # self.omsetJasa += ln.price_total
                            if issokpb:
                                if prodkpb == 'KPB':  # validasi tipe produk yg jasa / service utk oli khusus kpb
                                    x_omsetkpb += ln.price_unit * ln.quantity
                            elif id_product.x_dept == 'CR':
                                if v_work == 'Service Advisor' or v_work == 'Mekanik':
                                    # Update cr lagi
                                    x_cr += ln.quantity * ln.price_unit
                                    x_jmlcr += ln.quantity
                            else:
                                x_omsetjasa += ln.price_unit * ln.quantity
                                if ishr:
                                    x_jasahr += ln.price_unit * ln.quantity

                        else:  # validasi tipe produk yg stockable/sparepart
                            id_product.name
                            if categprod == 'Ahmpart':
                                # self.omsetPart += ln.price_total
                                x_omsetpart += ln.price_unit * ln.quantity
                            elif categprod == 'Oli':  # validasi tipe part yg kategori oli
                                if issokpb == 1:
                                    if prodkpb == 'KPB':  # validasi tipe produk yg jasa / service utk oli khusus kpb
                                        # self.omsetKpbOli += ln.price_total
                                        x_omsetkpboli += float(id_product.standard_price * ln.quantity)
                                else:
                                    # self.omsetPartOli += ln.price_total
                                    x_omsetpartoli += ln.price_unit * ln.quantity
                            elif categprod == 'Busi':  # validasi tipe part yg kategori busi
                                # self.omsetPartBusi += ln.price_total
                                x_omsetpartbusi += ln.price_unit * ln.quantity
                            else:
                                x_partall += ln.price_unit
                                # ambil nilai jasa khusus yg kpb
                                # ambil nilai jasa khusus yg CR
                            # ambil nilai partnya

                if v_work == "Cuci":
                    if sl.x_user_cuci.name == v_name:
                        x_cucian += 1

                if sl.x_kpb == 1:
                    ass_1 += 1
                elif sl.x_kpb == 2:
                    ass_2 += 1
                elif sl.x_kpb == 3:
                    ass_3 += 1
                elif sl.x_kpb == 4:
                    ass_4 += 1
                # Kriteria HR + GO + GP => HR
                else:
                    if sl.x_service == 'Lengkap':
                        x_sl += 1
                    elif sl.x_service == 'LR':
                        x_service_ringan += 1
                    elif sl.x_service == 'KPB':
                        x_service_ringan += 1
                    elif sl.x_service == 'GO':
                        x_totalgo += 1
                    elif sl.x_service == 'GOP':
                        x_qs += 1
                    elif sl.x_service == 'HR':
                        x_heavy_r += 1
                    elif sl.x_service == 'JR':
                        x_jr += 1
                    elif sl.x_service == 'SK':
                        x_sk += 1
                    elif sl.x_service == 'CL':
                        x_claim += 1
                    elif sl.x_service == 'OJ':
                        x_oj += 1
                    elif sl.x_service == 'SP':
                        x_sp += 1
                    else:
                        x_oj += 1

                if sl.x_antrian_service == 'BS':
                    x_bs += 1
                elif sl.x_antrian_service == 'FT':
                    x_ft += 1
                elif sl.x_antrian_service == 'Pit':
                    x_pit += 1
                else:
                    x_reguler += 1

            x_totalue = ass_1 + ass_2 + ass_3 + ass_4 + x_heavy_r + x_sl + x_qs + x_totalgo + x_jr + x_claim + x_sk \
                        + x_sp + x_oj + x_service_ringan
            # rekapitulasi data per nota per hari per mekanik

        simpanke = self.env['simontir.rekapproduktifitasharian'].sudo().create({
            "tanggal": v_tgllap, "bulan": "", "nama": v_name, "dept": v_dept,
            "jasa": x_omsetjasa + x_omsetkpb, "sparepart": x_omsetpart + x_partall,
            "oli": x_omsetpartoli + x_omsetkpboli, "busi": x_omsetpartbusi,
            "carbon_remover": x_cr, "unit_entri": x_totalue, "jmlCr": x_jmlcr,
            "ass1": ass_1, "ass2": ass_2, "ass3": ass_3, "ass4": ass_4, "go": x_totalgo, "hr": x_heavy_r,
            "sl": x_sl, "sr": x_service_ringan, "px": x_qs, "jr": x_jr, "cl": x_claim, "jasaHr": x_jasahr,
            "oj": x_oj, "sp": x_sp, "sk": x_sk, "cuci": x_cucian, "activiti": v_work})


class RekapProduktifitasHarian(models.Model):
    _name = 'simontir.rekapproduktifitasharian'

    tanggal = fields.Date()
    bulan = fields.Integer()
    nama = fields.Char()
    dept = fields.Char()
    jasa = fields.Float()
    sparepart = fields.Float()
    oli = fields.Float()
    busi = fields.Float()
    carbon_remover = fields.Float()
    unit_entri = fields.Integer()
    ass1 = fields.Integer()
    ass2 = fields.Integer()
    ass3 = fields.Integer()
    ass4 = fields.Integer()
    go = fields.Integer()
    hr = fields.Integer()
    sl = fields.Integer()
    sr = fields.Integer()
    px = fields.Integer()
    jr = fields.Integer()
    cl = fields.Integer()
    cuci = fields.Integer()
    activiti = fields.Char()


class updaterekapproduktifitas(models.Model):
    _inherit = 'simontir.rekapproduktifitasharian'

    oj = fields.Integer()
    sk = fields.Integer()
    sp = fields.Integer()

class updaterekapproduktifitas1(models.Model):
    _inherit = 'simontir.rekapproduktifitasharian'

    jasaHr = fields.Float()

class updaterekapproduktifitas2(models.Model):
    _inherit = 'simontir.rekapproduktifitasharian'

    jmlCr = fields.Float()