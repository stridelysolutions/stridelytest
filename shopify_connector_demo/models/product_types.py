from odoo import fields, models


class ProductTypes(models.Model):
    _name = 'product.types'
    _description = 'Product Types'
    _rec_name = "types_name"

    types_name = fields.Char(string='Product Types Name')
    