from re import template
import string

"""Driving School Students Attendance"""
import datetime
from odoo import models, fields, api

class students_attendance(models.Model):
    _name = "students.attendance"
    _description = 'students_attendance'
    
    students_attendance_id = fields.Many2one("driving_school.lessons")
    start_date = fields.Datetime(string="Start Date",related='students_attendance_id.start_date')
    end_date = fields.Datetime(string="End Date",related='students_attendance_id.end_date')
    email = fields.Char(string='Email')
    lessons_name = fields.Char(string="Lessons Name")
    name = fields.Char(string="Students") 
    attendance = fields.Selection(
        string='Attendance',
        selection=[('Present', 'Present'), ('Absent', 'Absent'),],
        default='Present'
    )
    state = fields.Char(string="State")
    bool_field = fields.Boolean('Same text', default=False) 
    
   
    def present_data(self):
        self.attendance = 'Present' 
        self.bool_field = True
        
        
    def absent_data(self):
        self.attendance = 'Absent' 
        self.bool_field = True  
        
    def correction_attendance(self):
        ctx={}
        search = self.env['driving_school.lessons'].search([('id','=',self.students_attendance_id.id)])
        ctx['email_from'] = self.env.user.company_id.email
        ctx['email_to'] = self.email
        template = self.env.ref("driving_school.email_template").id
        self.env['mail.template'].browse(template).send_mail(self.id, email_values=ctx,force_send=True)
