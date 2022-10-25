# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api, _

class ResConfigLaravel(models.Model):
    _inherit = "res.users"

    laravel_access_token = fields.Char(string="Access token")
    laravel_url = fields.Char(string="URL")

class OdoolaravelConnector(models.Model):
    _name = 'odoo.laravel.connector'
    _rec_name = 'access_token'

    access_token = fields.Char(string="Access token")
    requested_url = fields.Char(string='Requested URL')
    status = fields.Selection([
        ('disconnected', 'disconnected'),
        ('connected', 'Connected'),
    ], default='disconnected')

    _sql_constraints = [
        ('access_token', 'unique(access_token)', "the input token already exist")]

    def laravel_login(self):
        pass
    def laravel_logout(self):
        pass

