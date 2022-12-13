# -*- coding: utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import ValidationError
import requests


class ResPartner(models.Model):
   _inherit = 'res.partner'
      
   active_whatsapp = fields.Boolean(
       string='Active Whatsapp',
   )   
   active_wati_contacts = fields.Boolean(
       string='Active Wati Contacts',
       compute="check_wati_contacts",
       readonly=False
   ) 
   whatsapp_no = fields.Char(
       string='Whatsapp No',
   )
    
   def change_active_whatsapp(self):
        whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
        token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
        end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
        if whats_app:
            if not end_point or not token:
                raise ValidationError("Please enter End Point or Token")
            else:
                if self.whatsapp_no:
                    url = "https://"+end_point+"/api/v1/addContact/"+self.whatsapp_no
                    payload = {"customParams": [
                        {
                            "name":'name',
                            "value": self.name
                        },
                    ]}
                    headers = {
                        "content-type": "text/json",
                        "Authorization": token,
                    }
                    response = requests.post(url,json=payload,headers=headers)
                else:
                    raise ValidationError("Please enter WhatsApp Number")
          
   @api.depends('active_wati_contacts')
   def check_wati_contacts(self):
        whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
        token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
        end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
        if whats_app:
            if not end_point or not token:
                raise ValidationError("Please enter End Point or Token")
            else:
                url = "https://"+end_point+"/api/v1/getContacts"
                headers = {"Authorization": token}
                response = requests.get(url, headers=headers)
                for partner in self:
                    for contact in response.json()['contact_list']:
                        if contact['phone'] == partner.whatsapp_no:
                            partner.write({
                                'active_wati_contacts':True
                            })
