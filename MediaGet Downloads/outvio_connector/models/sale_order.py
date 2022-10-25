# -*- coding: utf-8 -*-
from odoo import models, api
from ..integration.api_client import OutvioApiClient


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        OutvioApiClient(self.env).send_order_to_outvio(res)
        return res

    def write(self, vals):
        for order in self:
            super(SaleOrder, order).write(vals)
            OutvioApiClient(self.env).send_order_to_outvio(order)
