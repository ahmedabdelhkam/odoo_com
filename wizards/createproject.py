from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
class createwizard(models.TransientModel):
    _name = 'create_wizard'
    project_name = fields.Many2one('realestate.formation', string="Project name")
    notes = fields.Char(string="Notes")

    def create_prjecto(self):
        data = {
            'model': 'realestate.formation',
            'form': self.read()[0]
        }
        selected_project = data['form']['project_name'][0]
        # projects = self.env['realestate.engineers'].search([('project', '=', selected_project)])
        projects = self.env['realestate.formation'].search([('id', '=', selected_project)])
        # print("projects", projects)
        data['docs'] = projects
        return self.env.ref('Realestate.create_project_report').report_action(self, data=data)



