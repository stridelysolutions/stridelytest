# -*- coding: utf-8 -*-

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    whats_app = fields.Boolean(string="Whats App" ,config_parameter='whatsapp_odoo.whats_app')
    token_key = fields.Char(string="Access Token",config_parameter='whatsapp_odoo.token_key')
    end_point = fields.Char(string="Api Endpoint",config_parameter='whatsapp_odoo.end_point')
