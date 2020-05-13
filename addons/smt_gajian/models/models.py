# -*- coding: utf-8 -*-s
from flectra import models, fields, api
import datetime 
from datetime import datetime, timedelta
from flectra.tools.safe_eval import safe_eval

class smtgajian(models.Model):
    _name = 'smt_gajian.smtgajian'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    tanggal = fields.Date()
     

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


    @api.multi
    def hitungInsentif(self):
        # fungsi untuk menghitung insentif harian utk semua
        # jabatan
        # hitung insentif jasanya
        # self.hitungInsentif(v_tgllap, v_name, v_dept, v_dept, v_work, x_totalue, totJasa, totPart, x_cr)
        # dx = datetime.strptime(self.tanggal, '%Y-%m-%d')
        pargj  = self.env['smt_gajian.pargaji'].sudo().search([('company', '=', self.env.user.company_id.name)])
        lninsentif  = self.env['simontir.rekapproduktifitasharian'].search([('tanggal', '>=', self.tanggal),
                                                                            ('tanggal', '<=', self.tanggal2)])
        isMinggu = False


        if lninsentif.exists():
            for lins in lninsentif:
                isMinggu = False
                x_ins_jasa = 0
                x_ins_part = 0
                x_ins_cr = 0
                x_inscuci = 0
                x_ins_ue = 0
                x_totalpart = 0
                x_jasahr = 0
                x_cr = 0
                da = datetime.strptime(lins.tanggal, '%Y-%m-%d')
                namahari = da.weekday()
                if namahari == 6:
                    isMinggu = True

                x_totalpart = lins.sparepart + lins.oli + lins.busi
                # activity mekanik

                if lins.activiti == "Mekanik":
                    if int(lins.jasa) < pargj.rjasamek1:    # 360000  10000
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasamek) * pargj.pxjasamek1
                    elif pargj.rjasamek1 < int(lins.jasa) < pargj.rjasamek3:    # 360000 - 479000 2000
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasamek) * pargj.pxjasamek2
                    elif pargj.rjasamek3 < int(lins.jasa) < pargj.rjasamek4:    # 480000 - 600000 3000
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasamek) * pargj.pxjasamek3
                    elif int(lins.jasa) > pargj.rjasamek4:                      # 600000  4000
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasamek) * pargj.pxjasamek4
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspamek1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspamek1/100)
                    elif pargj.rspamek1 < int(x_totalpart) < pargj.rspamek2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspamek2/100)
                    elif int(x_totalpart) > pargj.rspamek2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspamek3/100)
                    x_cr = lins.jmlCr

                    if 1 <= x_cr < pargj.rcrmek1:
                        x_ins_cr = pargj.pxcrmek1 * x_cr
                    elif pargj.rcrmek1 <= x_cr < pargj.rcrmek2 - 0.1:
                        x_ins_cr = pargj.pxcrmek2 * x_cr
                    elif x_cr >= pargj.rcrmek2:
                        x_ins_cr = pargj.pxcrmek3 * x_cr

                    x_jasahr = lins.jasaHr * (pargj.pxhr / 100)

                # hitung insentif unit entri harian
                    if 1 <= lins.unit_entri < pargj.ruemek1:
                        x_ins_ue = pargj.pxuemek1 * lins.unit_entri
                    elif pargj.ruemek1 <= lins.unit_entri < pargj.ruemek2:
                        x_ins_ue = pargj.pxuemek2 * lins.unit_entri
                    elif lins.unit_entri >= pargj.ruemek2:
                        x_ins_ue = pargj.pxuemek3 * lins.unit_entri

                elif lins.activiti == "Final Check":
                # hitung insentif jasa
                    if int(lins.jasa) < pargj.rjasasad1:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad1
                    elif pargj.rjasasad1 < int(lins.jasa) < pargj.rjasasad3:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad2
                    elif pargj.rjasasad3 < int(lins.jasa) < pargj.rjasasad4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad3
                    elif int(lins.jasa) > pargj.rjasasad4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad4
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspafisa1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa1/100)
                    elif pargj.rspafisa1 < int(x_totalpart) < pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa2/100)
                    elif int(x_totalpart) > pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa3/100)
                elif lins.activiti == "Service Advisor":
                    if int(lins.jasa) < pargj.rjasasad1:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad1
                    elif pargj.rjasasad1 < int(lins.jasa) < pargj.rjasasad4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad2
                    elif pargj.rjasasad3 < int(lins.jasa) < pargj.rjasasad4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad3
                    elif int(lins.jasa) > pargj.rjasasad4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasasad) * pargj.pxasasad4
                
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspafisa1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa1/100)
                    elif pargj.rspafisa1 < int(x_totalpart) < pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa2/100)
                    elif int(x_totalpart) > pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa3/100)
                # hitung insentif CR
                    x_cr = lins.jmlCr
                    if 1 <= x_cr < pargj.rcrsa1:
                        x_ins_cr = pargj.pxcrsa1 * x_cr
                    elif pargj.rcrsa1 <= x_cr < pargj.rcrsa2:
                        x_ins_cr = pargj.pxcrsa2 * x_cr
                    elif x_cr >= pargj.rcrsa2:
                        x_ins_cr = pargj.pxcrsa3 * x_cr

                elif lins.activiti == "Admin":
                # insentif jasa kasir,front desk
                    if int(lins.jasa) < pargj.rjasafde1:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde1
                    elif pargj.rjasafde1 < int(lins.jasa) < pargj.rjasafde3:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde2
                    elif pargj.rjasafde3 < int(lins.jasa) < pargj.rjasafde4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde3
                    elif int(lins.jasa) > pargj.rjasafde4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde4
                
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspafisa1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa1/100)
                    elif pargj.rspafisa1 < int(x_totalpart) < pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa2/100)
                    elif int(x_totalpart) > pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa3/100)
                elif lins.activiti == "Kasir":
                # insentif jasa kasir,front desk
                    if int(lins.jasa) < pargj.rjasafde1:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde1
                    elif pargj.rjasafde1 < int(lins.jasa) < pargj.rjasafde3:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde2
                    elif pargj.rjasafde3 < int(lins.jasa) < pargj.rjasafde4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde3
                    elif int(lins.jasa) > pargj.rjasafde4:
                        x_ins_jasa = (int(lins.jasa)/pargj.pjasafde) * pargj.pxasafde4
                
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspafisa1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa1/100)
                    elif pargj.rspafisa1 < int(x_totalpart) < pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa2/100)
                    elif int(x_totalpart) > pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa3/100)
                elif lins.activiti == "Partman":
                # insentif jasa partman tidak dapat
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspafisa1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa1/100)
                    elif pargj.rspafisa1 < int(x_totalpart) < pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa2/100)
                    elif int(x_totalpart) > pargj.rspafisa2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspafisa3/100)
                # belum include yang ada di POS dan Mutasi

                elif lins.activiti == "Kabeng":
                    if int(lins.jasa) < pargj.rjasakbe1:
                        x_ins_jasa = (int(lins.jasa)) * (pargj.pxjasakbe1/100)
                    elif pargj.rjasakbe1 < int(lins.jasa) < pargj.rjasakbe3:
                        x_ins_jasa = (int(lins.jasa)) * (pargj.pxjasakbe2/100)
                    elif pargj.rjasakbe3 < int(lins.jasa) < pargj.rjasakbe4:
                        x_ins_jasa = (int(lins.jasa)) * (pargj.pxjasakbe3/100)
                    elif int(lins.jasa) > pargj.rjasakbe4:
                        x_ins_jasa = (int(lins.jasa)) * (pargj.pxjasakbe4/100)
                # hitung insentif part
                    if int(x_totalpart) < pargj.rspakbe1:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspakbe1/100)
                    elif pargj.rspakbe1 < int(x_totalpart) < pargj.rspakbe2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspakbe2/100)
                    elif int(x_totalpart) > pargj.rspakbe2:
                        x_ins_part = (int(x_totalpart)) * (pargj.pxspakbe3/100)
                elif lins.activiti == "Cuci":
                    x_inscuci = lins.cuci * pargj.pxcuci

                if isMinggu:
                    x_ins_jasa = 0



                simpanke = self.env['smt_gajian.insentifharian'].sudo().create({
                                "tanggal": lins.tanggal, "nama": lins.nama, "dept": lins.dept,
                            "jasa": lins.jasa, "sparepart": x_totalpart, "ins_other3": x_jasahr,"ins_ue": x_ins_ue,
                            "cr": lins.jmlCr, "unit_entri": lins.unit_entri, 'cuci': lins.cuci,"ins_cuci":x_inscuci,
                            "ins_jasa": x_ins_jasa, "ins_part":x_ins_part, "ins_cr":x_ins_cr, "activiti": lins.activiti})   

class InsentifHarian(models.Model):
    _name = 'smt_gajian.insentifharian'

    tanggal = fields.Date()
    bulan = fields.Integer()
    nama = fields.Char()
    nik  = fields.Char()
    dept = fields.Char()
    activiti = fields.Char()
    jasa = fields.Float()
    sparepart = fields.Float()
    cr = fields.Float()
    unit_entri = fields.Integer()
    cuci = fields.Integer()
    ins_jasa = fields.Float()
    ins_part = fields.Float()
    ins_cr = fields.Float()
    ins_other1 = fields.Float()
    ins_other2 = fields.Float()
    ins_other3 = fields.Float()

class addFieldInsentif1(models.Model):
    _inherit = 'smt_gajian.insentifharian'

    ins_cuci = fields.Float()

class addFieldUeInsentifHarian(models.Model):
    _inherit = 'smt_gajian.insentifharian'

    ins_ue = fields.Float()


class rekapGaji(models.Model):
    _name = 'smt_gajian.rekapgaji'

    tanggal1 = fields.Date()
    tanggal2 = fields.Date()
    bulan = fields.Integer()
    periode = fields.Char()
    totalgaji = fields.Float()
    is_mekanik = fields.Boolean()
    is_admin = fields.Boolean()
    is_service_advisor = fields.Boolean()
    is_final_inspeksi = fields.Boolean()
    rumus_1 = fields.Char()
    rumus_2 = fields.Char()
    rumus_3 = fields.Char()
    rumus_4 = fields.Char()
    rumus_5 = fields.Char()
    rumus_6 = fields.Char()
    rumus_7 = fields.Char()
    rumus_8 = fields.Char()
    is_paid = fields.Boolean()
    

    @api.multi
    def prosespyr(self):
        # dx = datetime.strptime(self.tanggal1, '%Y-%m-%d')
        # dy = datetime.strptime(self.tanggal2, '%Y-%m-%d')
        # hitung total CR disini dulu
        insentifcr = self.env['smt_gajian.insentifharian'].search([('tanggal', '>=', self.tanggal1), ('tanggal', '<', self.tanggal2),
                                                                 ('activiti', '=', 'Mekanik')])
        pyrgj = self.env['smt_gajian.pargaji'].sudo().search([('company', '=', self.env.user.company_id.name)])

        x_ue = 0
        x_cr = 0
        for icr in insentifcr:
            x_cr += icr.cr
            x_ue += icr.unit_entri
        # tentukan nilai pengali CR nya
        self.tot_ue_bln = x_ue
        self.tot_cr_bln = x_cr

        if x_cr < pyrgj.rcrmek1:
            self.pxcrmek_bln = pyrgj.pxcrmek1
        elif pyrgj.rcrmek1 < x_cr < pyrgj.rcrmek2:
            self.pxcrmek_bln = pyrgj.pxcrmek2
        elif x_cr > pyrgj.rcrmek2:
            self.pxcrmek_bln = pyrgj.pxcrmek3

        if x_cr < pyrgj.rcrsa1:
            self.pxcrsa_bln = pyrgj.pxcrsa1
        elif pyrgj.rcrsa1 < x_cr < pyrgj.rcrsa2:
            self.pxcrsa_bln = pyrgj.pxcrsa2
        elif x_cr > pyrgj.rcrsa2:
            self.pxcrsa_bln = pyrgj.pxcrsa3

        totalmekanik = self.prosespyrmekanik(self.tanggal1, self.tanggal2, True, True, True)
        totaladmin = self.prosespyradmin(self.tanggal1, self.tanggal2, True, True)
        totalmanagement = self.prosespyrmanagement(self.tanggal1, self.tanggal2, True, False, False)

        self.totalgaji = totalmekanik + totaladmin + totalmanagement

    def prosespyrmekanik(self, d1, d2, ismekanik, isserviceadvisor, isfinalinspeksi):
        karyawan = self.env['hr.employee'].sudo().search([('company_id', '=', self.env.user.company_id.name),
                                                          ('job_id', 'in', ['ass mekanik','Mekanik','mekanik']), 
                                                          ('active', '=', 'True')])
        pyrgj  = self.env['smt_gajian.pargaji'].sudo().search([('company', '=', self.env.user.company_id.name)])

        dx = datetime.strptime(d1, '%Y-%m-%d')
        dy = datetime.strptime(d2, '%Y-%m-%d')
        x_total_terima = 0
        x_periode = ''
        #looping all mekanik + ass
        for lkar in karyawan:
            x_totjasa = 0
            x_totpart = 0
            x_tot_insjasa = 0
            x_tot_inspart = 0
            x_tot_inscr = 0
            x_tot_ue = 0
            x_tot_ue_sa = 0
            x_tot_ue_fi = 0
            x_tot_cr = 0
            x_tot_cuci = 0
            x_ins_other1 = 0
            x_ins_other2 = 0
            x_ins_other3 = 0
            x_ins_cuci = 0
            x_absen = 0
            #asumsi hanya activitas mekanik
            if ismekanik:
                insentif = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Mekanik')])
                for lins in insentif:
                    x_totjasa += lins.jasa
                    x_totpart += lins.sparepart
                    x_tot_ue += lins.unit_entri
                    x_tot_inscr += lins.ins_cr * self.pxcrmek_bln
                    x_tot_inspart += lins.ins_part
                    x_tot_insjasa += lins.ins_jasa
                    x_absen += 1

                #insentif  mekanik dan front desk berdasarkan total ue
                if  pyrgj.ruemek1 < x_tot_ue < pyrgj.ruemek2:
                    x_ins_other1 = pyrgj.pxuemek1
                elif pyrgj.ruemek2 < x_tot_ue < pyrgj.ruemek3:
                    x_ins_other1 = pyrgj.pxuemek2
                elif x_tot_ue > pyrgj.ruemek3:
                    x_ins_other1 = pyrgj.pxuemek3


                dw = datetime.strftime(dx, "%Y-%m-%d 00:00:00")
                du = datetime.strftime(dy, "%Y-%m-%d 23:59:59")
                insentifcuci = self.env['sale.order'].sudo().search([('confirmation_date', '>=', dw),
                                                                    ('confirmation_date', '<', du),
                                                                    ('state', '=', 'done'),
                                                                    ('company_id', '=', self.env.user.company_id.name),
                                                                    ('x_user_cuci', '=', lkar.name)])
                if insentifcuci.exists():
                    for lcuci in insentifcuci:
                        x_tot_cuci += 1

                    x_ins_cuci = x_tot_cuci * pyrgj.pxcuci
                
            if isserviceadvisor:
                insentif_sa = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Service Advisor')])
                for linsa in insentif_sa:
                    x_tot_ue_sa += linsa.unit_entri

                    #insentif  mekanik dan front desk berdasarkan total ue
                # x_ins_other2 = x_tot_ue_sa * 1000

            if isfinalinspeksi:
                insentif_fi = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Final Check')])
                for linfi in insentif_fi:
                    x_tot_ue_fi += linfi.unit_entri

                    #insentif  mekanik dan front desk berdasarkan total ue
                # x_ins_other3 = x_tot_ue * 500

            x_total_terima = lkar.timesheet_cost + x_tot_insjasa + x_tot_inspart + (x_tot_inscr) + x_ins_other1 + x_ins_other2 + x_ins_other3
            x_periode = "periodenya"
            simpankerekap = self.env['smt_gajian.detilgaji'].sudo().create({
                    "tanggal1": dy, "periode": x_periode,"bulan": "", "nama": lkar.name, "dept": lkar.department_id.name,
                    "gapok": lkar.timesheet_cost, "jabatan": lkar.job_id.name, "nik": lkar.barcode,
                    "totjasa": x_totjasa, "totsparepart": x_totpart, "kehadiran": x_absen,
                    "totcr": x_tot_inscr, "totue": x_tot_ue, "totcuci": x_tot_cuci,
                    "ins_jasa": x_tot_insjasa, "ins_part": x_tot_inspart, "ins_cr": x_tot_inscr, 
                    "ins_other1": x_ins_other1, "ins_other2": x_ins_other2, "ins_other3": x_ins_other3, 
                    "total_terima": x_total_terima})

        grandtotalmekanik =+ x_total_terima
        
        return grandtotalmekanik

    def prosespyradmin(self, d1, d2,isadmin, isserviceadvisor):
        karyawan = self.env['hr.employee'].sudo().search([('company_id', '=', self.env.user.company_id.name),
                                                          ('job_id', 'in', ['Staff', 'front desk', 'Partman','Service Advisor','Final Inspeksi']), 
                                                          ('active', '=', 'True')])
        pyrgj = self.env['smt_gajian.pargaji'].sudo().search([('company', '=', self.env.user.company_id.name)])

        dx = datetime.strptime(d1, '%Y-%m-%d')
        dy = datetime.strptime(d2, '%Y-%m-%d')
        x_total_terima = 0
        x_periode = ''
        for lkar in karyawan:
            x_totjasa = 0
            x_totpart = 0
            x_tot_insjasa = 0
            x_tot_inspart = 0
            x_tot_inscr = 0
            x_tot_ue = 0
            x_tot_ue_sa = 0
            x_tot_ue_fi = 0
            x_tot_cr = 0
            x_tot_cuci = 0
            x_ins_other1 = 0
            x_ins_other2 = 0
            x_ins_other3 = 0
            x_ins_cuci = 0
            x_absen = 0
            #asumsi hanya activitas admin
            if isadmin:
                insentif = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=', 'Admin')])
                for lins in insentif:
                    x_totjasa += lins.jasa
                    x_totpart += lins.sparepart
                    x_tot_ue += lins.unit_entri
                    x_tot_inscr += lins.ins_cr * self.pxcrsa_bln
                    x_tot_inspart += lins.ins_part
                    x_tot_insjasa += lins.ins_jasa
                    x_absen += 1

                #insentif  mekanik dan front desk berdasarkan total ue
                if pyrgj.rueflp1 < x_tot_ue < pyrgj.rueflp2:
                    x_ins_other1 = pyrgj.pxueflp1
                elif pyrgj.rueflp2 < x_tot_ue < pyrgj.rueflp3:
                    x_ins_other1 = pyrgj.pxueflp2
                elif x_tot_ue > pyrgj.rueflp3:
                    x_ins_other1 = pyrgj.pxueflp3
                
            if isserviceadvisor:
                insentif_sa = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Service Advisor')])
                for linsa in insentif_sa:
                    x_tot_ue_sa += linsa.unit_entri

                    #insentif  mekanik dan front desk berdasarkan total ue
                #x_ins_other2 = x_tot_ue_sa * 1000


            x_total_terima = lkar.timesheet_cost + x_tot_insjasa + x_tot_inspart + (x_tot_inscr) + x_ins_other1 + x_ins_other2 + x_ins_other3
            x_periode = "periodenya"
            simpankerekap = self.env['smt_gajian.detilgaji'].sudo().create({
                    "tanggal1": dy, "periode": x_periode,"bulan": "", "nama": lkar.name, "dept": lkar.department_id.name,
                    "gapok": lkar.timesheet_cost, "jabatan": lkar.job_id.name, "nik": lkar.barcode,
                    "totjasa": x_totjasa, "totsparepart": x_totpart, "kehadiran": x_absen,
                    "totcr": x_tot_inscr, "totue": x_tot_ue, "totcuci": x_tot_cuci,
                    "ins_jasa": x_tot_insjasa, "ins_part": x_tot_inspart, "ins_cr": x_tot_inscr, 
                    "ins_other1": x_ins_other1, "ins_other2": x_ins_other2, "ins_other3": x_ins_other3, 
                    "total_terima": x_total_terima})

        grandtotaladmin =+ x_total_terima
        
        return grandtotaladmin
        
    def prosespyrmanagement(self, d1, d2,ismekanik ,isserviceadvisor, isfinalinspeksi):
        karyawan = self.env['hr.employee'].sudo().search([('company_id', '=', self.env.user.company_id.name),
                                                          ('job_id', 'in', ['Kepala Bengkel', 'kepala bengkel']),
                                                          ('active', '=', 'True')])
        pyrgj = self.env['smt_gajian.pargaji'].sudo().search([('company', '=', self.env.user.company_id.name)])

        dx = datetime.strptime(d1, '%Y-%m-%d')
        dy = datetime.strptime(d2, '%Y-%m-%d')
        x_total_terima = 0
        x_periode = ''
        for lkar in karyawan:
            x_totjasa = 0
            x_totpart = 0
            x_tot_insjasa = 0
            x_tot_inspart = 0
            x_tot_inscr = 0
            x_tot_ue = 0
            x_tot_ue_sa = 0
            x_tot_ue_fi = 0
            x_tot_cr = 0
            x_tot_cuci = 0
            x_ins_other1 = 0
            x_ins_other2 = 0
            x_ins_other3 = 0
            x_ins_cuci = 0
            x_absen = 0
            x_printslip = ''
            #asumsi hanya activitas mekanik
            if ismekanik:
                insentif = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', 'in',['mekanik','Kabeng'])])
                for lins in insentif:
                    x_totjasa += lins.jasa
                    x_totpart += lins.sparepart 
                    x_tot_ue += lins.unit_entri
                    x_tot_inscr += lins.ins_cr
                    x_tot_inspart += lins.ins_part
                    x_tot_insjasa += lins.ins_jasa
                    x_absen += 1

                #insentif  mekanik dan front desk berdasarkan total ue
                if pyrgj.ruekbe1 < x_tot_ue < pyrgj.ruekbe2:
                    x_ins_other1 = pyrgj.pxuekbe1
                elif pyrgj.ruekbe2 < x_tot_ue < pyrgj.ruekbe3:
                    x_ins_other1 = pyrgj.pxuekbe2
                elif x_tot_ue > pyrgj.ruekbe3:
                    x_ins_other1 = pyrgj.pxuekbe3
                
            if isserviceadvisor:
                insentif_sa = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Service Advisor')])
                for linsa in insentif_sa:
                    x_tot_ue_sa += linsa.unit_entri

                    #insentif  mekanik dan front desk berdasarkan total ue
                #x_ins_other2 = x_tot_ue_sa * 1000

            if isfinalinspeksi:
                insentif_sa = self.env['smt_gajian.insentifharian'].search([('tanggal','>=', dx), ('tanggal','<', dy),
                                                                        ('nama', '=', lkar.name),
                                                                        ('activiti', '=','Final Check')])
                for linsa in insentif_sa:
                    x_tot_ue_sa += linsa.unit_entri

                    #insentif  mekanik dan front desk berdasarkan total ue
                #x_ins_other3 = x_tot_ue_sa * 1000

            x_total_terima = lkar.timesheet_cost + x_tot_insjasa + x_tot_inspart + (x_tot_inscr) + x_ins_other1 + x_ins_other2 + x_ins_other3
            x_periode = "periodenya"
            simpankerekap = self.env['smt_gajian.detilgaji'].sudo().create({
                    "tanggal1": dy, "periode": x_periode,"bulan": "", "nama": lkar.name, "dept": lkar.department_id.name,
                    "gapok": lkar.timesheet_cost, "jabatan": lkar.job_id.name, "nik": lkar.barcode,
                    "totjasa": x_totjasa, "totsparepart": x_totpart, "kehadiran": x_absen,
                    "totcr": x_tot_inscr, "totue": x_tot_ue, "totcuci": x_tot_cuci,
                    "ins_jasa": x_tot_insjasa, "ins_part": x_tot_inspart, "ins_cr": x_tot_inscr, 
                    "ins_other1": x_ins_other1, "ins_other2": x_ins_other2, "ins_other3": x_ins_other3, 
                    "total_terima": x_total_terima})

        grandtotalmanagement =+ x_total_terima
        
        return grandtotalmanagement

class detilGaji(models.Model):
    _name = 'smt_gajian.detilgaji'

    tanggal1 = fields.Date()
    bulan = fields.Integer()
    nama = fields.Char()
    nik  = fields.Char()
    dept = fields.Char()
    jabatan = fields.Char()
    gapok = fields.Float()
    kehadiran = fields.Integer()
    mangkir = fields.Integer()
    bt_makan = fields.Float()
    bt_transport = fields.Float()
    lembur = fields.Integer() 
    totjasa = fields.Float()
    totsparepart = fields.Float()
    totcr = fields.Float()
    totue = fields.Integer()
    totcuci = fields.Integer()
    ins_jasa = fields.Float()
    ins_part = fields.Float()
    ins_cr = fields.Float()
    ins_cuci = fields.Float()
    ins_other1 = fields.Float()
    ins_other2 = fields.Float()
    ins_other3 = fields.Float()
    ins_other4 = fields.Float()
    pot_1 = fields.Float()
    pot_2 = fields.Float()
    pot_3 = fields.Float()
    is_paid = fields.Boolean()
    printslip = fields.Text()
    total_terima = fields.Float(compute='_tot_terima', store=True)
    #baru
    tj_jabatan = fields.Float()
    tj_bpjs = fields.Float()
    bonus_thr = fields.Float()
    iuran_bpjs = fields.Float()
    

    @api.depends('ins_jasa','ins_part','ins_cr','ins_cuci','ins_other1','ins_other2','ins_other3','pot_1','pot_2','pot_3')
    def _tot_terima(self):
        for rec in self:
            rec.total_terima = (float(rec.gapok) + float(rec.bt_makan) + float(rec.bt_transport) + float(rec.ins_jasa) + float(rec.ins_part) + 
                            float(rec.ins_cr) + float(rec.ins_cuci) + float(rec.ins_other1) + float(rec.ins_other2) +
                            float(rec.ins_other3)) - (float(rec.pot_1) + float(rec.pot_2) + float(rec.pot_3))


class pargaji(models.Model):
    _name = 'smt_gajian.pargaji'

    #r untuk range, pb untuk pembagi,px untuk pengali
    #mekanik
    company = fields.Many2one('res.company', string='Perusahaan')
    tglberlaku = fields.Date(string= "Tanggal")
    #parameter harian jasa ---------
    pjasamek = fields.Float()
    rjasamek1 = fields.Float()
    rjasamek2 = fields.Float()
    rjasamek3 = fields.Float()
    rjasamek4 = fields.Float()
    pxjasamek1 = fields.Float()
    pxjasamek2 = fields.Float()
    pxjasamek3 = fields.Float()
    pxjasamek4 = fields.Float()
    #sa dan fi
    pjasasad = fields.Float()
    rjasasad1 = fields.Float()
    rjasasad2 = fields.Float()
    rjasasad3 = fields.Float()
    rjasasad4 = fields.Float()
    pxasasad1 = fields.Float()
    pxasasad2 = fields.Float()
    pxasasad3 = fields.Float()
    pxasasad4 = fields.Float()
    #fd dan kasir
    pjasafde = fields.Float()
    rjasafde1 = fields.Float()
    rjasafde2 = fields.Float()
    rjasafde3 = fields.Float()
    rjasafde4 = fields.Float()
    pxasafde1 = fields.Float()
    pxasafde2 = fields.Float()
    pxasafde3 = fields.Float()
    pxasafde4 = fields.Float()
    #kabeng
    pjasakbe = fields.Float()
    rjasakbe1 = fields.Float()
    rjasakbe2 = fields.Float()
    rjasakbe3 = fields.Float()
    rjasakbe4 = fields.Float()
    pxjasakbe1 = fields.Float()
    pxjasakbe2 = fields.Float()
    pxjasakbe3 = fields.Float()
    pxjasakbe4 = fields.Float()
    #--------Sparepart--------------
    #--------Mekanik---------
    rspamek1 = fields.Float()
    rspamek2 = fields.Float()
    rspamek3 = fields.Float()
    pxspamek1 = fields.Float()
    pxspamek2 = fields.Float()
    pxspamek3 = fields.Float()
    pxspamek4 = fields.Float()
    #--------SA dan FI---------
    rspafisa1 = fields.Float()
    rspafisa2 = fields.Float()
    rspafisa3 = fields.Float()
    pxspafisa1 = fields.Float()
    pxspafisa2 = fields.Float()
    pxspafisa3 = fields.Float()
    pxspafisa4 = fields.Float()
    #--------FD ---------------
    rspafd1 = fields.Float()
    rspafd2 = fields.Float()
    rspafd3 = fields.Float()
    pxspafd1 = fields.Float()
    pxspafd2 = fields.Float()
    pxspafd3 = fields.Float()
    pxspafd4 = fields.Float()
    #--------kasir ---------------
    rspaksr1 = fields.Float()
    rspaksr2 = fields.Float()
    rspaksr3 = fields.Float()
    pxspaksr1 = fields.Float()
    pxspaksr2 = fields.Float()
    pxspaksr3 = fields.Float()
    pxspaksr4 = fields.Float()
    #--------Partman ---------------
    rspaptm1 = fields.Float()
    rspaptm2 = fields.Float()
    rspaptm3 = fields.Float()
    pxspaptm1 = fields.Float()
    pxspaptm2 = fields.Float()
    pxspaptm3 = fields.Float()
    pxspaptm4 = fields.Float()
    #--------Kabeng ---------------
    rspakbe1 = fields.Float()
    rspakbe2 = fields.Float()
    rspakbe3 = fields.Float()
    pxspakbe1 = fields.Float()
    pxspakbe2 = fields.Float()
    pxspakbe3 = fields.Float()
    #--------Bulanan ---------------
    #--------Base on UE ---------------
    #--------Kasir,FD,SA,FI ---------------
    rueflp1 = fields.Float()
    rueflp2 = fields.Float()
    rueflp3 = fields.Float()
    pxueflp1 = fields.Float()
    pxueflp2 = fields.Float()
    pxueflp3 = fields.Float()
    #--------Mekanik---------------
    ruemek1 = fields.Float()
    ruemek2 = fields.Float()
    ruemek3 = fields.Float()
    pxuemek1 = fields.Float()
    pxuemek2 = fields.Float()
    pxuemek3 = fields.Float()
    #--------Kabeng---------------
    ruekbe1 = fields.Float()
    ruekbe2 = fields.Float()
    ruekbe3 = fields.Float()
    pxuekbe1 = fields.Float()
    pxuekbe2 = fields.Float()
    pxuekbe3 = fields.Float()
    #--------Insentif CR---------------
    pxcr = fields.Float()
    #--------Insentif Cuci---------------
    pxcuci = fields.Float()
    # --------Insentif Heavy Repair---------------
    pxhr = fields.Float()

    isactive = fields.Boolean()


class insentifaddtgl(models.Model):
    _inherit = 'smt_gajian.smtgajian'

    tanggal2 = fields.Date()


class addinsCR(models.Model):
    _inherit = 'smt_gajian.pargaji'

    # --------Mekanik---------------
    rcrmek1 = fields.Float()
    rcrmek2 = fields.Float()
    pxcrmek1 = fields.Float()
    pxcrmek2 = fields.Float()
    pxcrmek3 = fields.Float()
    # --------Service Advisor---------------
    rcrsa1 = fields.Float()
    rcrsa2 = fields.Float()
    pxcrsa1 = fields.Float()
    pxcrsa2 = fields.Float()
    pxcrsa3 = fields.Float()


class addfieldrekapGaji(models.Model):
    _inherit = 'smt_gajian.rekapgaji'

    tot_ue_bln = fields.Float()
    tot_cr_bln = fields.Float()
    tot_gaji_bln = fields.Float()
    pxcrmek_bln = fields.Float()
    pxcrsa_bln = fields.Float()
