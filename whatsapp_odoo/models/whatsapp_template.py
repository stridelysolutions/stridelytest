# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from bs4 import BeautifulSoup
from odoo.http import request
import requests,pdfkit
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class WhatsappTemplate(models.Model):
    _name = 'whatsapp.template'
    _rec_name = "subject"

    subject = fields.Char(string='Subject')
    list_id = fields.Many2one(
        string='Recipients',
        comodel_name='whatsapp.list',
    )
    template_id = fields.Many2one(
        string='Template',
        comodel_name='template.design',
    )
    body_html = fields.Html(string='Body converted to be sent by mail', sanitize=False ,compute="check_data")

    def send_msg(self):
        html_path = get_module_resource('whatsapp_odoo', 'static', 'template.html')
        pdf_path = get_module_resource('whatsapp_odoo', 'static', 'template.pdf')
        file = open(html_path,"w")
        file.write(self.template_id.body_html)
        file.close()  
        with open(html_path) as html_file:
            soup = BeautifulSoup(html_file.read(), features='html.parser')
            url = request.httprequest.host_url
            for tag in soup.find_all('img'):
                temp = tag['src']
                a = url[:len(url)-1] + temp
                tag['src'] = a
            new_text = soup.prettify()
        with open(html_path, mode='w') as new_html_file:
            new_html_file.write(new_text)
        for list in self.list_id:
            whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
            token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
            end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
            for recipient in list.customer_ids:
                if recipient.mobile:
                    pdfkit.from_file(html_path, pdf_path)
                    headers = {"Authorization": token}
                    url_file = "https://"+end_point+"/api/v1/sendSessionFile/"+str(recipient.mobile)
                    files = {"file": ("Template.pdf", open(pdf_path, "rb"), "application/pdf")}
                    response = requests.post(url_file,files=files, headers=headers)

    @api.depends('body_html','template_id')
    def check_data(self):
        for i in self:
            if i.template_id:
                i.template_id.body_arch
                i.write({
                    'body_html' :i.template_id.body_arch
                })
            else:
                i.body_html=''
