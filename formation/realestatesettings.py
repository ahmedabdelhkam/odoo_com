from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
class realestatesettings(models.TransientModel):
    _inherit = "res.config.settings"

    salary = fields.Char(string="Salary")
