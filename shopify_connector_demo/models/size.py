# -*- coding: utf-8 -*-
from odoo import fields,models


class Size(models.Model):
    """Product Size"""
    _name = "size.product"
    _description = "size Product"
    _rec_name = "size"


    size = fields.Char(string="Size")