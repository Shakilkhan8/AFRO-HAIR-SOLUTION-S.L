# -*- coding: utf-8 -*-
import logging
import time
import requests
from . import converters
from ..models.res_config_settings import API_TOKEN_KEY, DEBUG_MODE_KEY

_logger = logging.getLogger(__name__)


class OutvioApiClient:

    def __init__(self, env):
        self.env = env

    def send_order_to_outvio(self, order):
        if order.state == 'draft':
            return

        config = self.env['ir.config_parameter'].sudo()
        api_token = config.get_param(API_TOKEN_KEY)
        if api_token == 'Not set':
            _logger.warning('integration not set up')
            return

        payment_transaction = self.env['payment.transaction'].search(
            [('reference', '=', order.name), ('partner_id', '=', order.partner_id.id)], limit=1)
        payment = payment_transaction and {
            'method': payment_transaction.acquirer_id.name,
            'status': payment_transaction.state
        }

        description_by_order_line_id = self._get_product_descriptions(
            order.order_line)
        (invoicing_addr, delivery_addr) = self._get_addresses(order)
        payload = converters.order_to_json(
            order, invoicing_addr, delivery_addr, payment, description_by_order_line_id)
        payload['OUTVIO_PARAMS'] = {
            'API_KEY': api_token,
            'CMS_ID': 'odoo'
        }

        debug_mode = config.get_param(DEBUG_MODE_KEY, not False)
        url = config.get_param('outvio.api.url') + '/order'
        def request(): return requests.post(url=url, json=payload,
                                            headers={'Content-type': 'application/json'}, timeout=15)  # 15 seconds
        try:
            if debug_mode:
                self._execute_with_timer(request)
            else:
                request()
        except requests.ConnectionError:
            _logger.warning('cannot connect')
        except requests.Timeout:
            _logger.warning('response too long')
        except requests.HTTPError as e:
            _logger.warning('%s' % e)

    def _execute_with_timer(self, request):
        start_time = time.time()

        try:
            resp = request()
        except Exception as e:
            raise e
        else:
            _logger.info(resp)
            end_time = time.time()
            _logger.info('request took %s ms' %
                         round(end_time - start_time, 2))

    def _get_addresses(self, order):
        invoicing_addr = converters.partner_to_address(
            self.env['res.partner'].search([('id', '=', order.partner_invoice_id.id)], limit=1))
        delivery_addr = converters.partner_to_address(
            self.env['res.partner'].search([('id', '=', order.partner_shipping_id.id)], limit=1))

        return (invoicing_addr, delivery_addr)

    def _get_product_descriptions(self, order_lines):
        if not order_lines:
            return dict()

        self.env.cr.execute("""
        select sol.id, pt.description_sale
            from sale_order_line sol
            join product_product pp on sol.product_id = pp.id
            join product_template pt on pp.product_tmpl_id = pt.id
            where sol.id in %s; 
        """, (tuple([ol.id for ol in order_lines]),))

        return dict(self.env.cr.fetchall())
