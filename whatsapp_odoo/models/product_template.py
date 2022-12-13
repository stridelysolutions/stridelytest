# -*- coding: utf-8 -*-

try:
   import qrcode
except ImportError:
   qrcode = None
try:
   import base64
except ImportError:
   base64 = None
from io import BytesIO
from odoo import models,fields,api, _
from odoo.exceptions import UserError


class Product(models.Model):
   _inherit = "product.template"
   
   qr_code = fields.Binary('QRcode', compute="_generate_qr")

   def _generate_qr(self):
       "method to generate QR code"
       for rec in self:
           if qrcode and base64:
              
               qr = qrcode.QRCode(
                   version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=3,
                   border=4,
               )
               qr.add_data("https://25e1-203-88-138-162.in.ngrok.io")
               qr.make(fit=True)
               img = qr.make_image()
               temp = BytesIO()
               img.save(temp, format="PNG")
               qr_image = base64.b64encode(temp.getvalue())
               rec.update({'qr_code':qr_image})
           else:
               raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))
