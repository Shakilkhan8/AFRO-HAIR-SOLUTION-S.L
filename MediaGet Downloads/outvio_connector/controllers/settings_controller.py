# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json
import logging
from ..models.res_config_settings import API_TOKEN_KEY

_logger = logging.getLogger(__name__)


class OutvioSettingsController(http.Controller):
  @http.route('/outvio', auth='public', methods=['GET'], type='http')
  def handler(self, action):
    if action != 'getData':
      return Response(json.dumps({'success': False}), status=400, mimetype='application/json')

    return Response(json.dumps({'success': True, 'data': {
        'success': True,
        'shipping_methods': self._shipping_methods(),
        'payment_methods': self._payment_methods(),
        'statuses': self._order_statuses()
    }}), status=200, mimetype='application/json')

  def _shipping_methods(self):
    delivery_carriers = request.env['delivery.carrier'].sudo().search([
        ('active', '=', True)])
    return [{'id': c.name, 'name': c.name} for c in delivery_carriers]

  def _payment_methods(self):
    payment_acquirers = request.env['payment.acquirer'].sudo().search(
        [('state', '=', 'enabled')])
    return [{'id': str(p.id), 'name': p.name} for p in payment_acquirers]

  def _order_statuses(self):
    try:
      statuses = request.env['payment.transaction'].__class__.state.selection
      return [{'id': s[0], 'name': s[0]} for s in statuses]
    except Exception as e:
      _logger.error(e)
      return []
