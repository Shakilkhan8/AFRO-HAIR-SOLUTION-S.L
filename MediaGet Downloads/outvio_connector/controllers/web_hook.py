# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging
import hmac
import hashlib
from ..models.res_config_settings import API_TOKEN_KEY, API_URL_KEY, DEBUG_MODE_KEY

_logger = logging.getLogger(__name__)


class OutvioWebHook(http.Controller):
  @http.route('/outvio', auth='public', methods=['POST'], type='json', csrf=False)
  def handler(self):
    key = '!0utv10s3cr3t#'
    body = json.dumps(request.jsonrequest, separators=(',', ':'))
    digest = hmac.new(key.encode(), body.encode(), hashlib.sha256).hexdigest()

    params = request.httprequest.args
    token = params.get('token', '')
    action = params.get('action', '')

    if token != digest:
      return {
          'success': False,
          'message': 'Unauthorized'
      }

    api_token = request.jsonrequest.get('api_key', '')
    if not api_token:
      return {
          'success': False,
          'message': 'Missing Api Token'
      }

    if action == 'setConfig':
      api_mode = bool(request.jsonrequest.get('api_mode', 0))
      debug_mode = bool(request.jsonrequest.get('debug_mode', 0))
      self._setConfig(api_token, api_mode, debug_mode)

    return {
        'success': True
    }

  def _setConfig(self, apiToken, api_mode = False, debug_mode = False):
    _logger.info('updating Outvio config')
    config_params = request.env['ir.config_parameter'].sudo()
    if not config_params.get_param(API_TOKEN_KEY):
      _logger.error('plugin was not installed correctly')
      return
    config_params.set_param(API_TOKEN_KEY, apiToken)
    config_params.set_param(DEBUG_MODE_KEY, debug_mode)

    if api_mode:
      _logger.info('redirecting to DEV Api')
      config_params.set_param(API_URL_KEY, 'https://api.dev.outvio.com/v1')

    # request.env.cache.invalidate()
    config_params.invalidate_cache()
