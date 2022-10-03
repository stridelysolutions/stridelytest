import string
"""Driving School Services"""
from odoo import models, fields, api

class driving_school_services(models.Model):
    _name = "driving_school.services"
    _description = 'driving_school.services'

    name = fields.Char(string="Services Name")
