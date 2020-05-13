from datetime import datetime, timedelta
from flectra import models, fields, api

class WizardInsentif(models.TransientModel):
    _name = 'smt_gajian.wizardinsentif'

    tanggal = fields.Date()

    