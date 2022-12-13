# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TestTemplate(models.Model):
    _name = 'test.template'
    
    name = fields.Char(
        string='Name',
    )        
