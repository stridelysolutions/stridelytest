# -*- coding: utf-8 -*-
from odoo import fields,models


class Varients(models.Model):
    """Home dashbord"""
    _name = "products.varients"
    _description = "Product Varients"
    _rec_name = "varients_id"


    varients_id = fields.Many2one('shopify.products',string="Varients")
    color_id = fields.Many2one('color.product',string = "Product Color")
    product_size_id = fields.Many2one('size.product',string = "Product Size")
    product_image = fields.Binary(string="Product Image")