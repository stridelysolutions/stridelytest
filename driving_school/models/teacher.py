import string
"""Driving School Teacher"""
from odoo import models, fields

class driving_school_teacher(models.Model):
    _name = "driving_school.teacher"
    _description = 'driving_school.teacher'

    name = fields.Char(string="Services Name")
    password = fields.Char(string = "Password")
