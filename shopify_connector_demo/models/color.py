# -*- coding: utf-8 -*-
from odoo import fields,models


class Color(models.Model):
    """Product Color"""
    _name = "color.product"
    _description = "Color Product"
    _rec_name = "color"


    color = fields.Char(string="Color")
