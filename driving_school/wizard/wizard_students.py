import string
"""Driving School Wizard Students"""
import datetime
from odoo import models, fields, api

class driving_school_wizard_students(models.Model):
    _name = "driving_school.wizard_students"
    _description = 'driving_school.wizard_students'

    students_ids = fields.Many2many('school.students',string="Students")

    def create_data(self):
        context = self.env.context.get('active_id')
        search_data = self.env['driving_school.classes'].search_read([('id','=',context)])
        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        duration =0
        from_date = []
        for i  in search_data:
        # count days
            if i['from_date'].month == i['to_date'].month:
                dcin = i['from_date']
                dcin = dcin.date()
                dcin = str(dcin).split('-')
                dcin = int(dcin[2])
                dcou = i['to_date']
                dcou = dcou.date()
                dcou = str(dcou).split('-')
                dcou = int(dcou[2])
                duration = dcou - dcin

            elif i['from_date'].month < i['to_date'].month:
                if i['from_date'].month - i['to_date'].month > 1:
                    m = i['from_date'].month - i['to_date'].month
                    mul = m * 30
                    duration = mul - i['from_date'].day + i['to_date'].day  
                     
            start_date = i['from_date']
            delta = datetime.timedelta(days=1)
            for j in range(duration+1):
                if i['repeats'] == 'weekly':
                    day = datetime.datetime.strptime(str(start_date),"%Y-%m-%d %H:%M:%S").weekday()
                    if i['monday'] == True and day_name[day] == 'Monday':
                        from_date.append(start_date)
                    if i['tuesday'] == True and day_name[day] == 'Tuesday':
                        from_date.append(start_date)
                    if i['wednesday'] == True and day_name[day] == 'Wednesday':
                        from_date.append(start_date)
                    if i['thursday'] == True and day_name[day] == 'Thursday':
                        from_date.append(start_date)
                    if i['friday'] == True and day_name[day] == 'Friday':
                        from_date.append(start_date)    
                    if i['saturday'] == True and day_name[day] == 'Saturday':
                        from_date.append(start_date) 
                    if i['sunday'] == True and day_name[day] == 'Sunday':
                        from_date.append(start_date)  
                    start_date += delta
                    
                if i['repeats'] == 'daily':
                    print("okkkk")
                    from_date.append(start_date)
                    start_date += delta
                    
            if i['repeats'] == 'monthly':
                search_month = self.env['driving_school.monthly'].search_read([('monthly_id','=',context)])
                for m in search_month:
                    from_date.append(m['monthly_date'])
                    
                    
        for k in from_date:           
           self.env['driving_school.lessons'].create({
                'lessons_name': search_data[0]['name'],
                'start_date':k,
                'end_date':k + datetime.timedelta(hours=2),
                'lessons_id' : context,
                'state':search_data[0]['state'],
                })  
        
        record_id = self.env['driving_school.lessons'].search([('lessons_id', '=', context)])
        for j in self.students_ids:
            record_id.write({'students_data_ids': [(4, j.id)]})
