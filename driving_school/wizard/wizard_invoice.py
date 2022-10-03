import string
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
"""Driving School Classes Report"""


class driving_school_wizard_students(models.Model):
    _name = "driving_school.wizard_invoice"
    _description = 'driving_school.wizard_invoice'
    
    amount = fields.Float(string='Amount',required=True)
    def create_invoice(self):
        ids = []
        context=self.env.context.get("active_id")
        invoice_students = self.env['driving_school.lessons'].search([('lessons_id','=',context)])
        count_invoice = self.env['driving_school.classes'].browse(context)
        for i in invoice_students:
            for j in i.students_data_ids:
                ids.append(j.partner_id)
            break       
        for j in ids:        
            invoice_data = {
                'move_type':'out_invoice',    
                'invoice_partner_display_name':j.name,    
                'partner_id': j,
                'invoice_line_ids': [(0, 0, {'price_unit':self.amount,'product_id':invoice_students['product']} )]

            }
            cus_invoice = self.env['account.move'].create(invoice_data)
            count_invoice.write({'invoice_ids' : [(4,cus_invoice.id)]})
