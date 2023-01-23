from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class RealestateFormation(models.Model):
    _name = 'realestate.formation'
    _description = 'model to organise realestate offices'
    _rec_name = 'project_name'
    project_name = fields.Char(string='Project name')
    project_number = fields.Char(string='Project number')
    company_name = fields.Char(string='Company name')
    broker_name = fields.Char(string='Broker name')
    engineer_id = fields.Many2one('realestate.engineers', string='Engineer')
    name_seq = fields.Char(string='Order Reference', required='True', copy='False',
                           readonly='True', index='True', default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string='states', default='draft', readonly=True)
    realestate_descreption = fields.Text(string = "short note")
    project_assigned = fields.One2many('realestate.engineers', 'assigned_project', string="Engineers involved")
    user_id = fields.Many2one('res.users', string='pro')
    email_id = fields.Char(string="email")
    barcode = fields.Char('Barcode')
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New') == _('New')):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('realestate.sequence') or _('New')
        result = super(RealestateFormation, self).create(vals)
        return result

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'
        # print(self.project_assigned.ids)

    def action_done(self):
        self.state = 'done'
        # value = self.env['realestate.engineers'].browse([1, 2])
        # print(value)

    def action_cancel(self):
        self.state = 'cancel'

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s %s' % (rec.project_name, rec.company_name)))
        return res

class RealestateEngineers(models.Model):
    _name = 'realestate.engineers'
    _description = 'model to assign projects to Engineers'
    _rec_name = 'engineer_name'
    engineer_name = fields.Char(string='Engineer name')
    # project = fields.Many2one('realestate.formation', string='Project')
    name_seq = fields.Char(string='Order Reference', required='True', copy='False',
                           readonly='True', index='True', default=lambda self: _('New'))
    engineer_score = fields.Integer(string='Engineer score', required=True)
    engineer_grade = fields.Selection([
        ('senior', 'Senior'),
        ('junior', 'Junior')
          ], string='Engineer`s grade', compute='setgrade', default='junior')
    realestates_num = fields.Integer( compute='getnum')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')])
    table_descreption = fields.Text(string="short note")
    recomindations_descreption = fields.Text(string="Add yours")
    user_id = fields.Many2one('res.users', string='User')
    # active = fields.Boolean(string="Active")
    assigned_project = fields.Many2one('realestate.formation',string="for one to many")

    @api.depends('realestates_num')
    def getnum(self):
        count = self.env['realestate.formation'].search_count([('engineer_id', '=', self.id)])
        self.realestates_num = count

    @api.depends('engineer_score')
    def setgrade(self):
        for rec in self:
            if rec.engineer_score:
                if rec.engineer_score <= 5:
                    rec.engineer_grade = 'junior'
                else:
                    rec.engineer_grade = 'senior'

    @api.constrains('engineer_score')
    def checkscore(self):
        for rec in self:
            if rec.engineer_score:
                if rec.engineer_score > 10:
                    raise ValidationError('Engineers score must be between 0 to 10')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New') == _('New')):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('engineer.sequence') or _('New')
        result = super(RealestateEngineers, self).create(vals)
        return result


    def realestate(self):
        return {
            'name': _('Realestates'),
            'domain': [('engineer_id', '=', self.id)],
            # 'view_type': 'form',
            'res_model': 'realestate.formation',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'


class CountEngineers(models.Model):
    _name = 'count.engineers'
    _description = 'model to organize financial administration'
    _rec_name = 'salary'
    engineer_name = fields.Many2one('realestate.engineers', string="Engineer name")
    salary = fields.Integer(string="Salary")



class RealestateInheritance(models.Model):
    _inherit = 'sale.order'
    engineer_name = fields.Char(string='Engineer name')
