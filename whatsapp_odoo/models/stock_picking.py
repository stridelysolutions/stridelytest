# -*- coding: utf-8 -*-

from odoo import models
import requests,json
from odoo.http import request
from odoo.exceptions import ValidationError


class StockPicking(models.TransientModel):
    _inherit = 'stock.immediate.transfer'
    
    def process(self):
        res = super(StockPicking, self).process()
        whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
        token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
        end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
        search = self.env['stock.picking'].browse(self.env.context.get('button_validate_picking_ids'))
        url_link = request.httprequest.host_url
        if whats_app:
            if not end_point or not token:
                raise ValidationError("Please enter End Point or Token")
            else:
                message_data = "Hi" + " " + search.partner_id.name + ',' + '\n\n' + "We are glad to inform you that your order n°"+ search.origin +" has been shipped."
                url = "https://"+end_point+"/api/v1/sendSessionMessage/"+str(search.partner_id.mobile)+"?messageText="+message_data
                headers = {"Authorization": token}
                response = requests.post(url, headers=headers)
        return res
