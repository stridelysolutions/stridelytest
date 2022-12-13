# -*- coding: utf-8 -*-

from odoo import models,fields
import requests,json
from odoo.http import request
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    token_key = fields.Char(
        string='field_name',
    )
     
    def action_send_whatsapp(self):
        compose_form_id = self.env.ref('whatsapp_odoo.whatsapp_message_wizard_form').id
        ctx = dict(self.env.context)
        message = "Hi" + " " + self.partner_id.name + ',' + '\n' + "Your quotation" + ' ' + self.name + ' ' + "amounting" + ' ' + str(
            self.amount_total) + self.currency_id.symbol + ' ' + "is ready for review.Do not hesitate to contact us if you have any questions."
        ctx.update({
            'default_message': message,
            'default_partner_id': self.partner_id.id,
            'default_mobile': self.partner_id.mobile,
            'default_image_1920': self.partner_id.image_1920,
            'sale_id':self.id
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'whatsapp.message.wizard',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
        token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
        end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
        url_portal = self.get_portal_url()
        url = request.httprequest.host_url
        if whats_app:
            if not end_point or not token:
                raise ValidationError("Please enter End Point or Token")
            else:
                message_data = "Hi" + " " + self.partner_id.name + ',','','' + '\n' + "Your Order are confirmed " + self.name + " is ready for review. "+'\n\n'+url[:len(url)-1]+url_portal+'\n\n'+"Do not hesitate to contact us if you have any questions."
                if self.state == 'sale':
                    url = "https://"+end_point+"/api/v1/sendSessionMessage/"+str(self.partner_id.mobile)+"?messageText="+message_data
                    headers = {"Authorization": token}
                    response = requests.post(url, headers=headers)
        return res
