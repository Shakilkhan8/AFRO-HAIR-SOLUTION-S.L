# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api, _


class LaravelInheritProductCategory(models.Model):
    _inherit = "product.category"
    unique_id = fields.Char(required=False)


class LaravelInheritProductBrand(models.Model):
    _inherit = "product.brand"
    unique_id = fields.Char(required=False)


class LaravelInheritProductAttribute(models.Model):
    _inherit = "product.attribute.value"
    unique_id = fields.Char(required=False)


class LInheritProductAttrVals(models.Model):
    _inherit = "product.attribute"
    unique_id = fields.Char(required=False)


class LaravelInheritProductTemplate(models.Model):
    _inherit = "product.template"

    unique_id = fields.Char(required=False)

    @api.model
    def create(self, vals):
        res = super(LaravelInheritProductTemplate, self).create(vals)
        product_product = self.env['product.product'].search([('product_tmpl_id', '=', res.id)])
        product_product.unique_id = res.unique_id
        return res


class LaravelInheritProductProduct(models.Model):
    _inherit = "product.product"

    unique_id = fields.Char(required=False)


class LaravelInheritSaleOrder(models.Model):
    _inherit = "sale.order"

    unique_id = fields.Char(required=False)


class LaravelConnectorOperations(models.TransientModel):
    _name = 'laravel.connector.operations'

    name = fields.Selection(string="Select Operation",
                            selection=[('p_variant', 'Product Variant'), ('p_category', 'Product Category'),
                                       ('p_brand', 'Product Brand'), ('product', 'Product'), ('orders', 'Orders')],
                            required=True, )

    def create_product_category(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.category'].search([]).mapped('unique_id')
                    if not rec['unique_id'] in unique_id:
                        category = self.env['product.category'].create({
                            'name': rec['name'],
                            'unique_id': rec['unique_id']
                        })
                    if rec['subcatagory']:
                        if sub_category:
                            parent_category_for_sub = category.id
                        else:
                            parent_category_for_sub = self.env['product.category'].search(
                                [('unique_id', '=', rec['unique_id'])]).id
                        for subcateg in rec['subcatagory']:
                            if not subcateg['unique_id'] in unique_id:
                                sub_category = self.env['product.category'].create({
                                    'name': subcateg['name'],
                                    'parent_id': parent_category_for_sub,
                                    'unique_id': subcateg['unique_id']
                                })
                            if subcateg['subtosub_catagory']:
                                if sub_category:
                                    parent_category_for_sub_sub = sub_category.id
                                else:
                                    parent_category_for_sub_sub = self.env['product.category'].search(
                                        [('unique_id', '=', subcateg['unique_id'])]).id
                                for subsubcateg in subcateg['subcatagory']:
                                    if not subsubcateg['unique_id'] in unique_id:
                                        sub_sub__category = self.env['product.category'].create({
                                            'name': subsubcateg['name'],
                                            'parent_id': parent_category_for_sub_sub,
                                            'unique_id': subsubcateg['unique_id']
                                        })

    def create_product_variant(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.attribute'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        create_attr = self.env['product.attribute'].create({
                            'name': rec['Name'],
                            'unique_id': str(rec['id']),
                            # 'value_ids': values_list
                        })
                    if rec['varientvalue']:
                        for vals in rec['varientvalue']:
                            attr_value = self.env['product.attribute.value'].search([]).mapped('name')
                            if not vals['name'] in attr_value:
                                create_attr_value = self.env['product.attribute.value'].create({
                                    'name': vals['name'],
                                    'unique_id': str(vals['id']),
                                    'attribute_id': create_attr.id,
                                })

    def create_product_brand(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.brand'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        self.env['product.brand'].create({
                            'name': rec['name'],
                            'unique_id': rec['id']
                        })

    def create_product(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.template'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        create_product = self.env['product.template'].create({
                            'name': rec['title'],
                            'unique_id': rec['id'],
                            'barcode': rec['sku'],
                        })

    def create_orders(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['sale.order'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        create_order = self.env['sale.order'].create({
                            'partner_id': 7,
                            'unique_id': rec['id'],
                        })
                        if rec['product_details']:
                            for line in rec['product_details']:
                                prod = self.env['product.product'].search(
                                    [('unique_id', '=', line['id'])])
                                if prod:
                                    line = self.env['sale.order.line']
                                    create_order.write({
                                        'order_line': [(0, 0, {
                                            'product_id': prod.id,
                                            'name': 'test',
                                        })],
                                    })
                                o = 'done'

    def sync_action(self):
        for rec in self:
            if rec.name == 'p_category':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-category/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_category(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'p_brand':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-brand/')
                    collected_data = request_data.json().get('data')
                    rec.create_product_brand(collected_data)
                except Exception as e:
                    print(e)

            if rec.name == 'p_variant':
                request_data = requests.post(url='https://mastbeauty.com/api/get-varients/')
                collected_data = request_data.json().get('data')
                rec.create_product_variant(collected_data)

            if rec.name == 'product':
                request_data = requests.post(url='https://mastbeauty.com/api/get-product/')
                collected_data = request_data.json().get('data')
                rec.create_product(collected_data)

            if rec.name == 'orders':
                request_data = requests.post(url='https://mastbeauty.com/api/Order/List/All/')
                collected_data = request_data.json().get('data')
                rec.create_orders(collected_data)
