# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api, _


class LaravelInheritContacts(models.Model):
    _inherit = "res.partner"

    shipp_addr = fields.Char('Shipping Address', required=False)
    bill_addr = fields.Char('Billing Address', required=False)
    unique_id = fields.Char(required=False)


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
    prod_template = fields.Many2one("product.template", string="Product Template", required=False, )


class LaravelInheritSaleOrder(models.Model):
    _inherit = "sale.order"

    unique_id = fields.Char(required=False)
    shipping_addr = fields.Char('Shipping Address', required=False, )
    billing_addr = fields.Char('Billing Address', required=False)
    laravel_order_status = fields.Selection(string="", selection=[('PENDING', 'Pending'), ('FAILED', 'Failed'),
                                                                  ('DELIVERED', 'Delivered'),
                                                                  ('CANCELLED', 'Cancelled')], required=False, )


class LaravelConnectorOperations(models.TransientModel):
    _name = 'laravel.connector.operations'

    name = fields.Selection(string="Select Operation",
                            selection=[('customer', 'Customers'), ('p_variant', 'Product Variant'),
                                       ('p_category', 'Product Category'),
                                       ('p_brand', 'Product Brand'), ('product', 'Product'), ('orders', 'Orders')],
                            required=True, )

    def create_laravel_customers(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['res.partner'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        if rec['addresses']:
                            shipping_address = rec['addresses'][0].get('address_line1')
                        else:
                            shipping_address = 'no address'
                        if rec['billingaddresses']:
                            billing_address = rec['billingaddresses'][0].get('address_line1')
                        else:
                            billing_address = 'no address'

                        self.env['res.partner'].create({
                            'name': rec['name'],
                            'unique_id': rec['id'],
                            'shipp_addr': shipping_address,
                            'bill_addr': billing_address,
                        })

    def create_product_category(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['product.category'].search([]).mapped('unique_id')
                    if not rec['unique_id'] in unique_id:
                        category = self.env['product.category'].create({
                            'name': rec['name'],
                            'unique_id': rec['unique_id'],
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
                    if rec:
                        try:
                            variant_data = rec['varients']
                            variant_attributes = dict()
                            for var in variant_data:
                                if str(var.get('varient_type_id')) in variant_attributes:
                                    list_vals = variant_attributes[str(var.get('varient_type_id'))]
                                    variant_attributes[str(var.get('varient_type_id'))] = list_vals + [
                                        var.get('varient_value_id')]
                                else:
                                    variant_attributes[str(var.get('varient_type_id'))] = [var.get('varient_value_id')]

                            # -----------------attribute_line_ids -----------------------------------------
                            attr_line_list = []
                            variants_ids_list = []
                            attribute_values_ids = []
                            for attr, value in variant_attributes.items():
                                attribute_id = self.env['product.attribute'].search([('unique_id', '=', int(attr))])
                                for val in value:
                                    val_id = self.env['product.attribute.value'].search([('unique_id', '=', val)]).id
                                    if val_id:
                                        attribute_values_ids.append(val_id)
                                        variants_ids_list.append(val)
                                # attribute_values_ids = [
                                #     self.env['product.attribute.value'].search([('unique_id', '=', val)]).id for val in
                                #     value if self.env['product.attribute.value'].search([('unique_id', '=', val)]).id]

                                attr_line_list.append(
                                    (0, 0, {'attribute_id': attribute_id.id, 'value_ids': attribute_values_ids}))
                        except Exception as e:
                            raise models.ValidationError(
                                f"Something went in attributes {rec['id']}, {e}")

                        unique_id = self.env['product.template'].search([]).mapped('unique_id')
                        if not str(rec['id']) in unique_id:
                            prod_vals = {
                                'name': rec['title'],
                                'unique_id': rec['id'],
                                'barcode': rec['sku'],
                                'detailed_type': 'product',
                                # 'brand_id' : int(rec['brand'])
                            }

                            if attr_line_list:
                                prod_vals['attribute_line_ids'] = attr_line_list

                            try:
                                create_product = self.env['product.template'].create(prod_vals)
                            except Exception as e:

                                raise models.ValidationError(
                                    f"Something went in product create {rec['id'], e}")

                        variants = create_product.product_variant_ids
                        if rec['varients'] and variants:

                            for vr in variants:
                                for vd in variant_data:
                                    if vd['varient_value_id'] in variants_ids_list:
                                        vd_product_attribute = self.env['product.attribute'].search(
                                            [('unique_id', '=', vd['varient_type_id'])])
                                        vd_attribute_value_name = [i.name for i in vd_product_attribute.value_ids if
                                                                   int(i.unique_id) == vd['varient_value_id']]
                                        try:
                                            if vd_product_attribute.name == vr.attribute_line_ids.display_name and \
                                                    vd_attribute_value_name[0] == vr.product_template_attribute_value_ids.name:
                                                location = self.env.ref('stock.stock_location_stock')

                                                self.env['stock.quant']._update_available_quantity(vr, location,
                                                                                                   float(vd['stock']))
                                                vr.update({
                                                    'standard_price': float(vd['mrp_price']),
                                                    'lst_price': float(vd['sell_price']),
                                                    # 'unique_id': str(vd['id'])

                                                    # 'qty_available': float(vd['stock'])
                                                })
                                        except Exception as e:
                                            raise models.ValidationError(
                                                f"Something went in update quantity {rec['id']}")
                        attr_line_list.clear()
                        variants_ids_list.clear()
                        attribute_values_ids.clear()





    def create_orders(self, *data):
        if data:
            for li in data:
                for rec in li:
                    unique_id = self.env['sale.order'].search([]).mapped('unique_id')
                    if not str(rec['id']) in unique_id:
                        partner_rec = self.env['res.partner'].browse(int(rec['user_id']))
                        create_order = self.env['sale.order'].create({
                            'partner_id': partner_rec.id,
                            'unique_id': rec['id'],
                            'laravel_order_status': rec['status'],
                            'shipping_addr': partner_rec.shipp_addr,
                            'billing_addr': partner_rec.bill_addr,
                        })
                        try:
                            if rec['product_details']:
                                for dic in rec['product_details']:
                                    prod = self.env['product.product'].search(
                                        [('unique_id', '=', dic['id'])], limit=1)
                                    if prod:
                                        line = self.env['sale.order.line']
                                        create_order.write({
                                            'order_line': [(0, 0, {
                                                'product_id': prod.id,
                                                'name': prod.display_name,
                                                'product_uom_qty': float(dic['quantity']),
                                                'price_unit': float(dic['sold_price'])
                                            })],
                                        })
                                if rec['status'] == 'DELIVERED':
                                    create_order.action_confirm()
                                    create_order.picking_ids._action_done()
                                    create_order._create_invoices()

                        except Exception as e:
                            raise models.ValidationError(
                                f"Something went in line {rec['id']}")


    def sync_action(self):
        for rec in self:

            if rec.name == 'orders':
                request_data = requests.post(url='https://mastbeauty.com/api/Order/List/All/')
                collected_data = request_data.json().get('data')
                rec.create_orders(collected_data)

            if rec.name == 'customer':
                try:
                    request_data = requests.post(url='https://mastbeauty.com/api/get-users/')
                    collected_data = request_data.json().get('data')
                    rec.create_laravel_customers(collected_data)
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
