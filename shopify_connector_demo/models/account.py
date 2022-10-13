# -*- coding: utf-8 -*-
from odoo import fields,models
import http.client
import json
import base64
import requests


class Accountaccess(models.Model):
  """account login"""
  _name = "account.access"
  _description = "Api account page"
  _rec_name = "store_name"
  
  
  vendor_name = fields.Many2one('res.partner',string="Vendor Name")
  store_name = fields.Char(string="Store Name")
  api_token = fields.Char(string="API Token Id")
  
  
  def sync_product(self):
    list_products = []
    list_product_name = []
    products_desc = []
    list_img = []
    
    conn = http.client.HTTPSConnection(self.store_name+".myshopify.com")
    payload = ''
    headers = {
      'Content-Type': 'application/json',
      'X-Shopify-Access-Token': self.api_token
    }
    conn.request("GET", "/admin/api/2022-07/products.json", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    json_data = data.decode("utf-8")
    json_load = json.loads(json_data)
    # json_products = json_load["products"]
    for i in json_load["products"]:
      # print(i["id"])
      # print(i["title"])
      json_image = i["images"]
      # null_data = (json_image == [])
      # if null_data == True:
      #   print("NNNNNNNNNNNNN",null_data)
      for img in json_image:
        img_data = base64.b64encode(requests.get(img['src'].strip()).content).replace(b'\n', b'')
        # print("++++++",img_data)
        list_img.append(img_data)
      
      
      list_product_name.append(i["title"])
      list_products.append(i["id"])
      products_desc.append(i["body_html"])
      
    # print("******?",list_img)
    # print(list_product_name)
    
    products = []
    products_ids = self.env['product.template'].search([])
    for p in products_ids:    
      products.append(p.name)
      # print("============YES GOT IT",products)  
      
    products_res = [x for x in list_product_name + products if x not in products]
    print("============YES",products_res)
    if products_res:
      for name,desc,sale_desc in zip(products_res,list_products,products_desc):
        print(name,desc,sale_desc)
        self.env['product.template'].create({'name':name,'description':desc,'description_sale':sale_desc})
    else:
      print("products upto date")
