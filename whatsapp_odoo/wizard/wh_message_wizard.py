

from odoo import models, fields, api
import requests,base64,PyPDF2
from xlrd import open_workbook
import io


class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.message.wizard'

    partner_id = fields.Many2one('res.partner', string="Recipient")
    mobile = fields.Char(required=True, string="Contact Number")
    message = fields.Text(string="Message", required=True)
    image_1920 = fields.Binary(readonly=1)    
    attachment_ids = fields.Many2many(
        string='Attach A File',
        comodel_name='ir.attachment',
    )
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        sale_id = self.env.context.get('sale_id')
        self.mobile = self.partner_id.mobile
        self.image_1920 = self.partner_id.image_1920
        values = self.env['mail.compose.message'].generate_email_for_composer(
                12, [sale_id],
                ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc',  'reply_to', 'attachment_ids', 'mail_server_id']
            )[sale_id]
        attachment_ids = []
        Attachment = self.env['ir.attachment']
        for attach_fname, attach_datas in values.pop('attachments', []):
            data_attach = {
                'name': attach_fname,
                'datas': attach_datas,
                'res_model': 'mail.compose.message',
                'res_id': 0,
                'type': 'binary',
            }
            attachment_ids.append(Attachment.create(data_attach).id)
        self.attachment_ids = attachment_ids
        writer = PyPDF2.PdfFileWriter()
        reader = PyPDF2.PdfFileReader(io.BytesIO(base64.b64decode(self.attachment_ids.datas)), strict=False, overwriteWarnings=False)
        writer.addPage(reader.getPage(0))
        output = open('/opt/odoo/custom/whatsapp_odoo/static/test.pdf','wb')
        writer.write(output)
        output.close()
        
    def send_message(self):
        if self.message and self.mobile:
            sale_id = self.env['sale.order'].browse(self.env.context.get('sale_id')).name
            whats_app = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.whats_app')
            token = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.token_key')
            end_point = self.env['ir.config_parameter'].sudo().get_param('whatsapp_odoo.end_point')
            url = "https://"+end_point+"/api/v1/sendSessionMessage/"+str(self.mobile)+"?messageText="+self.message
            # url = "https://app-server.wati.io/api/v1/sendSessionMessage/%2B919724954105?messageText"
            headers = {"Authorization": token}
            response = requests.post(url, headers=headers)
            url_file = "https://"+end_point+"/api/v1/sendSessionFile/"+str(self.mobile)
            files = {"file": (sale_id+".pdf", open("/opt/odoo/custom/whatsapp_odoo/static/test.pdf", "rb"), "application/pdf")}
            headers = headers
            response = requests.post(url_file,files=files, headers=headers)
            print("===//===")
