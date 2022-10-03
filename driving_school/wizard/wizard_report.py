import string
"""Driving School Classes Report"""
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class driving_school_wizard_students(models.Model):
    _name = "driving_school.wizard_report"
    _description = 'driving_school.wizard_report'
    
    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To") 
    lessons = fields.Selection([
         ('started', 'Started'),
         ('completed', 'Completed'),
         ('Both Started and Completed','Both Started and Completed'),
         ],'Lessons Type', default='started')
    classes = fields.Many2many(
         'driving_school.classes',
         string="Classes(s)"
         )

    @api.onchange('lessons')
    def change_data(self):
         if self.lessons == 'started' or self.lessons == 'completed':
               classes = self.env['driving_school.classes'].search([('state','=',self.lessons)])
               self.write({
                    'classes': [(6,0, classes.ids)],
               })
         elif self.lessons == 'Both Started and Completed':
              classes = self.env['driving_school.classes'].search(['|',('state','=','started'),('state','=','completed')]) 
              self.write({
                    'classes': [(6,0, classes.ids)],
               })     

    def search_data(self):
        month = self.from_date.strftime("%B") 
        day=self.to_date - self.from_date
        
        if day.days >= 0:
          if self.lessons == 'started' or self.lessons == 'completed':
               search_data = self.env['driving_school.lessons'].search_read([('start_date','>=',self.from_date),('end_date','<=',self.to_date),('state','=',self.lessons)])
          elif self.lessons == 'Both Started and Completed':
               search_data = self.env['driving_school.lessons'].search_read([('start_date','>=',self.from_date),('end_date','<=',self.to_date),'|',('state','=','started'),('state','=','completed')])    
          start_date = self.from_date
          delta = datetime.timedelta(days=1)
          date = []
          days_name =[]
          day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
          
          for i in range(day.days+1):
               date.append(start_date.strftime('%d'))
               day = datetime.datetime.strptime(str(start_date),"%Y-%m-%d").weekday()
               days_name.append(day_name[day])
               start_date += delta
               
          data={}
          data2={}
          for d in search_data:
               if d['lessons_name'] not in data:
                    name = []
                    for n in d['students_data_ids']:
                         search = self.env['school.students'].search_read([('id','=',n)])
                         name.append(search[0]['name'])
                    data[d['lessons_name']] = name
         
          return self.env.ref('driving_school.action_classes_id_html_card').report_action(self , data={
                    'model':'driving_school.wizard_report',
                    'form':data,
                    'month':month,
                    'date':date,
                    'days_name': days_name,
               })       
        else:       
             raise ValidationError((f'Please Enter proper date'))     
