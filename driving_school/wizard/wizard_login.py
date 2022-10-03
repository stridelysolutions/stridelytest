import string
"""Driving School Login Teacher"""
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class driving_school_wizard_students(models.Model):
    _name = "driving_school.login"
    _description = 'driving_school.login'
    
    username = fields.Char(string="Username")
    password = fields.Char(string="Password")
    
    def check_data(self):
        context=self.env.context.get("active_id")
        search = self.env['driving_school.teacher'].\
            search_read(['&',('name','=',self.username),\
                ('password','=',self.password)])
        if search:
            search_id = self.env['students.attendance'].search([('id','=',context)])
            search_id.write({
                'bool_field':False,
            })
        else:
             raise ValidationError((f'Please Enter proper date'))     
