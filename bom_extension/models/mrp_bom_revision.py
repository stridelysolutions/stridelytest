import string
from odoo import models, fields, api
import datetime
"""Mrp Bom Revision"""


class mrp_bom_revision(models.Model):
    _name = 'mrp.bom.revision'
    
    no = fields.Integer(string = "Revision")
    author = fields.Many2one("res.users",string="Author")
    modification_date = fields.Date(string = 'Modification Date' ,default=fields.Datetime.now)
    modification_name = fields.Text(string = 'Modification Name')
    revision_id = fields.Many2one('mrp.bom') 