import string
"""Driving School Lessons"""
from odoo import models, fields
import random


class driving_school_lessons(models.Model):
    _name = "driving_school.lessons"
    _description = 'driving_school.lessons'
    _rec_name = 'lessons_name'
     
    lessons_name = fields.Char(string="Lesson Name")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    state = fields.Char(string = "State")    
    lessons_id = fields.Many2one("driving_school.classes")
    teacher = fields.Many2one('driving_school.teacher',string="Teacher",related='lessons_id.teacher')
    service = fields.Many2one('driving_school.services',string="Service",related='lessons_id.service')
    vehicle =  fields.Many2one('fleet.vehicle',string = "Vehicle",related='lessons_id.vehicle')
    product = fields.Many2one('product.product',related='lessons_id.product')
    students_data_ids = fields.Many2many('school.students',string="Students")
    students_attendance_ids = fields.One2many('students.attendance','students_attendance_id',string="Attendance")
    state = fields.Selection([('draft','Draft'),('started','Started'),('completed','Completed'),('cancelled','Cancelled')],default='draft',string='Status')
       
    def start_data(self):
        self.state="started"
        search_data = self.env['driving_school.lessons'].search_read([('id','=',self.id)])
        for i in search_data:
          
            for j in i['students_data_ids']:
                search_data_student = self.env['school.students'].search_read([('id','=',j)])
                self.env['students.attendance'].create({
                'name': search_data_student[0]['name'],
                'students_attendance_id' : self.id,
                'state':search_data[0]['state'],
                'lessons_name':search_data[0]['lessons_name'],
                'email': search_data_student[0]['email']
                })

    def complete_data(self):
        self.state="completed" 
        
    def cancel(self):
        self.state="cancelled" 
