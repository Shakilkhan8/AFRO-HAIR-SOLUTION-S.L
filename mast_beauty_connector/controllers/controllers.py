from odoo import http, models
from odoo.http import request

from odoo.http import request
import json


# $$$$$$$$$$$$$$    MAST CONNECTOR AUTHENTICATION    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class MastBeautyConnectorController(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        session_details = request.env['ir.http'].session_info()
        return session_details

    @http.route('/create/customer', type='json', auth='user')
    def mast_beauty_create_customer(self, **rec):
        create_customer = request.env['res.partner'].create({
            'name': rec.get('name'),
            'email': rec.get('email') if rec.get('email') else False,
            'mobile': rec.get('mobile') if rec.get('mobile') else False,
            'title': rec.get('title') if rec.get('title') else False,
            'function': rec.get('function') if rec.get('function') else False,
            'phone': rec.get('phone') if rec.get('phone') else False,
            'street': rec.get('street') if rec.get('street') else False,
            'city': rec.get('city') if rec.get('city') else False,
            'country_id': rec.get('country_id') if rec.get('country_id') else False,
            'zip': rec.get('zip') if rec.get('zip') else False,
        })
        if create_customer:
            return {'message': 'Record Created Successfully', 'id': create_customer.id}
        else:
            return {'message': 'Record Not Created'}

    @http.route('/update/customer', type='json', auth='user')
    def mast_beauty_update_customer(self, **rec):
        create_customer = request.env['res.partner'].browse(rec.get('id'))
        del rec['id']
        if create_customer:
            create_customer.update(rec)
            return {'id': 'success'}

    @http.route('/list/customers', type='json', auth='user')
    def list_customers(self):
        lst_customer = []
        student_rec = request.env['res.partner']
        models_ids = request.env['res.partner'].search([])
        for model in models_ids:
            new_dict = model.read(list(set(student_rec._fields)))
            lst_customer.append(new_dict)

        return {'result': lst_customer}


        # std_list = []
        # for rec in student_rec:
        #     std_dic = {
        #         'id': rec.id,
        #         'name': rec.name,
        #         'email': rec.email,
        #         'mobile': rec.mobile,
        #         'title': rec.title,
        #         'phone': rec.phone,
        #         'street': rec.street,
        #         'city': rec.city,
        #         'country': rec.country_id.name,
        #         'zip': rec.zip,
        #     }
        #     std_list.append(std_dic)
        # return std_list

    @http.route('/web/get/product/category', type='json', auth='user')
    def get_mast_product_category(self):
        prod_categ_rec = request.env['product.category'].search([])
        product_categ_list = [{
            'id': rec.id,
            'name': rec.name,
            'parent_id': rec.parent_id.id,
            'parent_name': rec.parent_id.name,
            'costing_method': rec.property_cost_method,
            'inventory_valuation': rec.property_valuation,
            'income_account_name': rec.property_account_income_categ_id.name,
            'income_account': rec.property_account_income_categ_id.id,
            'expense_account_name': rec.property_account_expense_categ_id.name,
            'expense_account': rec.property_account_expense_categ_id.id

        } for rec in prod_categ_rec]

        return product_categ_list

    @http.route('/create/product/category', type='json', auth='user')
    def create_product_category(self, **rec):
        if rec:
            create_prod_category = request.env['product.category'].create({
                'name': rec.get('name'),
                # 'parent_id': rec.get('parent_id'),
                # 'property_cost_method': rec.get('costing_method'),
                # 'property_valuation': rec.get('inventory_valuation'),

            })
        return {'id': create_prod_category.id}

    # Create Product attribute
    @http.route('/create/product/attribute', type='json', auth='user')
    def create_product_attribute(self, **rec):
        if rec:
            attribute = request.env['product.attribute'].create({
                'name': rec.get('name'),
                'value_ids': [(0, 0, {'name': val.get('name')}) for val in rec.get('value_ids')]
            })
        return {'id': attribute.id}

    # View Product attributes
    @http.route('/view/product/attribute', type='json', auth='user')
    def view_product_attribute(self):
        attribute = request.env['product.attribute'].search([])
        record = [{
            'id': rec.id,
            'name': rec.name,
            'value_ids': [{'id': vals.id, 'name': vals.name} for vals in rec.value_ids]
        } for rec in attribute ]
        return {'record': record}

    @http.route('/create/product/template', type='json', auth='user')
    def create_product_template(self, **rec):
        if rec:
            vals = {
                'name': rec.get('name'),
                'list_price': rec.get('sale_price'),
                'standard_price': rec.get('cost_price'),
                'attribute_line_ids': [(0, 0, {'attribute_id': attr.get('attribute_id'), 'value_ids': attr.get('value_ids')}) for attr in rec.get('attribute_line_ids')],
            }
            create_prod_category = request.env['product.template'].create(vals)
            return {'id': create_prod_category.id, 'product_variant_ids': create_prod_category.product_variant_ids.ids}

    @http.route('/view/product/template', type='json', auth='user')
    def search_product_template(self):
        lst_product = []
        prod_obj = request.env['product.template']
        models_ids = request.env['product.template'].search([])
        for model in models_ids:
            new_dict = model.read(list(set(prod_obj._fields)))
            lst_product.append(new_dict)

        return {'result': lst_product}


    @http.route('/update/product/template', type='json', auth='user')
    def update_product_template(self, **rec):
        if rec:
            update_product = request.env['product.template'].browse(rec.get('id'))
            del rec['id']
            if update_product:
                update_product.update(rec)
                return {'id': 'success'}


    @http.route('/web/get/product/variants', type='json', auth='user')
    def get_product_category(self):
        prod_template_rec = request.env['product.product'].search([])
        product_template_list = [{
            'id': rec.id,
            'name': rec.name,
            'can_be_sold': rec.sale_ok,
            'can_be_purchase': rec.purchase_ok,
            'product_type': rec.type,
            'product_category_id': rec.categ_id.id,
            'sale_price': rec.list_price,
            'cost_price': rec.standard_price,
        } for rec in prod_template_rec]

        return product_template_list


    @http.route('/update/product/variants/id', type='json', auth='user')
    def update_product_variants_id(self, **rec):
        product_var = request.env['product.product'].browse(rec.get('id'))
        del rec['id']
        if product_var:
            product_var.update(rec)
            return {'id': 'success'}

