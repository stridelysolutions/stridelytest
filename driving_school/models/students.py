import string
"""Driving School Students"""
from odoo import models, fields, api
import datetime

class driving_school_students(models.Model):
    _name = "school.students"
    _description = 'school.students'
    
    title = fields.Char(string="Title")
    name = fields.Char(string="Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    blood_group = fields.Char(string="Blood Group")
    emergency_contact = fields.Char(string = "Emergency Contact")
    nationality = fields.Char(string = "Nationality")
    language = fields.Char(string = "Language")
    lessons=fields.Many2many('driving_school.lessons',string="Lessons")
    count_data = fields.Integer(string="Count" , compute = "count_lessons_number" ,default=0)
    gender= fields.Selection([('Male','Male'),('Female','Female')])
    image = fields.Binary(string="Image")
    partner_id = fields.Many2one('res.partner', string="Customer")
    color = fields.Integer(string='Color Index', default=0)
    email = fields.Char(string="Email")
    check = fields.Boolean(string = "Check")
    user = fields.Many2one('res.users',string= "User")
    
    @api.onchange('name','lessons')
    def search_lessons(self):
         return {'domain': {'lessons': [('students_data_ids.name', '=', self.name)]}}
     
    def count_lessons_number(self):
        for i in self:
           i.count_data=len(i.lessons)
    
    @api.model
    def create(self, vals):
        print("vals",vals)
        partner_vals={
            'name':vals['name']
        }
        partne_id = self.env['res.partner'].create(partner_vals)
        vals['partner_id']=partne_id.id
        print("vals['partner_id']",vals['partner_id'])
        return super(driving_school_students, self).create(vals)      
    
    def check_status(self):
        print("done") 
        
    def test_email(self):
        search = self.env['school.students'].search([])
        for i in search:
            for j in i.lessons:
                print(i.email)
                print(j.start_date)
                ctx={}
                if j.start_date.date() == datetime.datetime.now().date():
                    print(i.id)
                    ctx['email_from'] = self.env.user.company_id.email
                    ctx['email_to'] = i.email
                    template = self.env.ref("driving_school.email_template_reminder").id
                    self.env['mail.template'].browse(template).send_mail(i.id, email_values=ctx,force_send=True)
