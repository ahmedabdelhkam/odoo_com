from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
class countwizard(models.TransientModel):
    _name = 'count.wizard'
    engineer_name = fields.Many2one('realestate.engineers', string="Engineer name")
    salary = fields.Integer(string="Salary")

    def create_count(self):
        vals = {
            'engineer_name': self.engineer_name.id,
            'salary': self.salary
        }
        self.env['count.engineers'].create(vals)
    # In course he uses for rec in self but it's not necessary because wizard has only one instance .
    def delete_count(self):
        self.engineer_name.unlink()
