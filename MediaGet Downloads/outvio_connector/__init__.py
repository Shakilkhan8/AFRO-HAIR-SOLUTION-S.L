# -*- coding: utf-8 -*-
from . import controllers
from . import models
import logging
from odoo import api, SUPERUSER_ID
from .models.res_config_settings import API_TOKEN_KEY, API_URL_KEY

_logger = logging.getLogger(__name__)


def populate_api_url_hook(cr, register):
    _logger.info('Setting up Outvio integration')
    env = api.Environment(cr, SUPERUSER_ID, {})
    config = env['ir.config_parameter'].sudo()
    config.set_param(API_URL_KEY, 'https://api.outvio.com/v1')
    config.set_param(API_TOKEN_KEY, 'Not set')


def clear_api_token_hook(cr, register):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].sudo().set_param(API_TOKEN_KEY, None)
