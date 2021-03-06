# See LICENSE file for full copyright and licensing details.

from flectra import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    over_credit = fields.Boolean('Allow Over Credit?')
