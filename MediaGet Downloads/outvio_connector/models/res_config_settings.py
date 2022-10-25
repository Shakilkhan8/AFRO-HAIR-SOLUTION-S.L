# -*- coding: utf-8 -*-
from odoo import models, fields

API_URL_KEY = 'outvio.api.url'
API_TOKEN_KEY = 'outvio.api.token'
DEBUG_MODE_KEY = 'outvio.debug.mode'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outvio_api_url = fields.Char(
        string='Outvio Api Url', required=True, config_parameter=API_URL_KEY)
    outvio_api_token = fields.Char(
        string='Outvio Api Token', required=True, config_parameter=API_TOKEN_KEY)

    outvio_debug_mode = fields.Boolean(
        string='Outvio Debug Mode', default=False, required=False, config_parameter=DEBUG_MODE_KEY)
