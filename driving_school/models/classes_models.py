# -*- coding: utf-8 -*-
"""Driving School Classes Model"""
from odoo import models, fields, api
import datetimel
from odoo.exceptions import ValidationError


class driving_school_classes(models.Model):
    _name = 'driving_school.classes'
    _description = 'driving_school.classes'

    name = fields.Char(string="Name",required=True)
    from_date = fields.Datetime(string = "From" ,default=fields.Datetime.now)
    to_date = fields.Datetime(string="To" ,default=fields.Datetime.now)
    vehicle =  fields.Many2one('fleet.vehicle',string = "Vehicle")
    location = fields.Many2one('res.country',string="Location")
    available_spaces = fields.Integer(string="Available Spaces")
    service = fields.Many2one('driving_school.services',string="Service")
    teacher = fields.Many2one('driving_school.teacher',string="Teacher") 
    repeats = fields.Selection(
        string='Repeats',
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),('monthly','Monthly')],
        default = 'daily'
    )
    sunday = fields.Boolean('Sunday',default=False)
    monday = fields.Boolean('Monday',default=False)
    tuesday = fields.Boolean('Tuesday',default=False)    
    wednesday = fields.Boolean('Wednesday',default=False)
    thursday = fields.Boolean('Thursday',default=False)
    friday = fields.Boolean('Friday',default=False)
    saturday = fields.Boolean('Saturday',default=False)
    monthly_ids = fields.One2many('driving_school.monthly','monthly_id',string="Monthly Dates")
    lessons_ids = fields.One2many('driving_school.lessons','lessons_id')
    state = fields.Selection([
        ('draft','Draft'),
        ('started','Started'),
        ('completed','Completed'),
        ('cancelled','Cancelled')],
        default='draft',string='Status')
    count  = fields.Integer(String = "Count Record", compute='count_lessons',default=0)
    invoice_ids = fields.Many2many('account.move')
    count_invoice = fields.Integer(string="Invoice",default=0 , compute='invoice_data_id')
    product = fields.Many2one('product.product')
    active = fields.Boolean(string="Active",default=True)
    
    
    def start_data(self):
        self.state="started"
        self.state_data()
        
    def complete_data(self):
        self.state="completed" 
        self.state_data()
         
    def cancel(self):
        self.state="cancelled" 
        self.state_data()    
        
    def count_lessons(self):
        for i in self:
            i.count = self.env['driving_school.lessons'].search_count([('lessons_id', '=', i.id)])

    def state_data(self):
        for i in self.lessons_ids:
            if i.start_date.date() == datetime.datetime.now().date():
                record_id = self.env['driving_school.lessons'].search([('id', '=', i.id)])
                record_id.write({
                    'state': self.state
                    }) 
            
    def invoice_data_id(self):
        for i in self:
            i.count_invoice= len(i.invoice_ids)
    
    @api.model
    def create(self, vals):
        print("vals",vals)
        data_search = self.env['fleet.vehicle'].browse(vals['vehicle'])
        product_vals={
            'name':data_search.name
        }
        product_id = self.env['product.product'].create(product_vals)
        product = product_id
        return super(driving_school_classes, self).create(vals)            
            
    def create_invoice_data(self):
        action = self.env['ir.actions.actions']._for_xml_id("account.action_move_out_invoice_type")
        action.update(
                name='Invoice',
                domain=[('id','in',self.invoice_ids.ids)],
                res_model='account.move',)
        return action  
             
    @api.onchange('from_date','to_date')
    def check_date(self):
        day=self.to_date.date() - self.from_date.date()
        if day.days <0:
             raise ValidationError((f'Please Enter proper date'))   
