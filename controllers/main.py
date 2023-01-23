from odoo import http
from odoo.http import request


class RealestateController(http.Controller):

    @http.route('/relestate/showingup', auth='public', website=True)
    def realestate_show_up(self):
        projects = request.env['realestate.formation'].sudo().search([])
        return request.render('Realestate.w_template', {
            'projects': projects,
        })

class Realestatewebsite(http.Controller):

    @http.route('/create/newone', type='http', auth='public', website=True)
    def realestate_create_up(self):
        return 'hello'
        # projects = request.env['realestate.formation'].sudo().search([])
        # return request.render('Realestate.w_template', {
        #     'projects': projects,
        # })



class RealestateConfirm(http.Controller):

    @http.route('/create/project', type='http', auth='public', website=True)
    def realestate_create_confirm(self, **kwargs):
        print(kwargs)
        request.env['realestate.formation'].sudo().create(kwargs)
        # vals = {
        # 'engineer_name': kwargs.get('project_name'),
        # 'engineer_score': 6
        #  }
        # request.env['realestate.engineers'].sudo().create(vals)




class Realestatepasstwo(http.Controller):

    @http.route('/create/two', type='http', auth='public', website=True)
    def realestate_pass_up(self):
        projects = request.env['realestate.formation'].sudo().search([])
        print(projects[0])
        return request.render('Realestate.one_project', {
            'project_name': projects[0].project_name,
        })



