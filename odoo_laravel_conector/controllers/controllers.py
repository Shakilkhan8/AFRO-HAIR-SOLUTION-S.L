# -*- coding: utf-8 -*-
# from odoo import http


# class OdooLaravelConector(http.Controller):
#     @http.route('/odoo_laravel_conector/odoo_laravel_conector', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_laravel_conector/odoo_laravel_conector/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_laravel_conector.listing', {
#             'root': '/odoo_laravel_conector/odoo_laravel_conector',
#             'objects': http.request.env['odoo_laravel_conector.odoo_laravel_conector'].search([]),
#         })

#     @http.route('/odoo_laravel_conector/odoo_laravel_conector/objects/<model("odoo_laravel_conector.odoo_laravel_conector"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_laravel_conector.object', {
#             'object': obj
#         })
