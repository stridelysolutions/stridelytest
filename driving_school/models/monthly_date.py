import string
"""Driving School Monthly Date Classes"""
from odoo import models, fields

class driving_school_monthly_date(models.Model):
     _name = "driving_school.monthly"
     _description = 'driving_school.monthly'

     monthly_date = fields.Datetime(string= 'Monthly Dates')
     monthly_id = fields.Many2one('driving_school.classes')
     