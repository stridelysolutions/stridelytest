from email.policy import default
from itertools import product
from odoo import api,fields,models
import http.client
import json

class Products(models.Model):
    """Products"""
    _name = "shopify.products"
    _description = "shopify Products page"
    _rec_name = "product_name"
    

    product_name = fields.Many2one('product.template',string="Product")
    product_type = fields.Many2one('product.types',string = "Product Type")
    status = fields.Selection([
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Updated','Updated'),
        ('Deleted', 'Deleted')],
        string="Status",
        default="Draft"
        )
    vendor = fields.Char(string="Vendor")
    store_name = fields.Many2one('account.access',string="Store name")
    image = fields.Binary(string="Product Image")
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")
    compare_price = fields.Float(string="Compare Price")
    shopify_id = fields.Char(string="Shopify Id",readonly=True)
    variant_id = fields.Char(string = "Shopify Varient ID",readonly=True)
    image_id = fields.Char(string = "Shopify Image ID",readonly=True)
    color_ids = fields.Many2many('color.product',string = "Product Color")
    product_size_ids = fields.Many2many('size.product',string = "Product Size")
    varients_ids = fields.One2many('products.varients','varients_id',string="Varients Lines")
    
    
    def export_shopify(self):
        """Created Product export to shopify """
        self.status = "Sent"
        color_data = self.env['color.product'].search([])
        size_data = self.env['size.product'].search([])
        print("&&&&&&&",self.product_type.types_name)
        
        color_details = self.varients_ids
        
        #----------------------this is a varients details color code static---------------------------------
        colors = []
        color_data1 = [d for d in color_details[0].color_id]
        color_data2 = [d for d in color_details[1].color_id]
        for c1 in color_data1:
            colors.append(c1.color)
        for c2 in color_data2:
            colors.append(c2.color)
        # print("*******",colors[0])
        
        #---------------------this is a varients details size code static------------------------------------
        size = []
        size_data1 = [d for d in color_details[0].product_size_id]
        size_data2 = [d for d in color_details[1].product_size_id]
        for s1 in size_data1:
            size.append(s1.size)
        for s2 in size_data2:
            size.append(s2.size)
                
        #---------------------dynemic Store data in varients------------------------        
        # arr_varients = []
        # product_tmpl = self.env['product.template'].search_read([])
        # for product in product_tmpl.product_ids:
        #     arr_varients.append({
        #         "option1": product.color,
        #         "option2": size[0]
        #     })
        
        # print("*******",size[0])
        
        #-------------------DYNEMIC COLOR AND SIZE in option----------------
        arr_varient = []
        for d in self.varients_ids:
            # print("CCCCCCCCCCC_-----------",d.color_id.color)
            # print("SSSSSSSSSSS_-----------",d.product_size_id.size)
            arr_varient.append({
                    "option1": d.color_id.color,
                    "option2": d.product_size_id.size
                })
            # print("AAAA=======",arr_varient)
        

             
        #--------------------------Api Connection and create product in shopify----------------------------
        for i in self.store_name:
            conn = http.client.HTTPSConnection(i.store_name+".myshopify.com")
            payload = json.dumps({
            "product": {
                "title": self.product_name.name,
                "body_html": self.description,
                "vendor": self.vendor,
                "product_type": self.product_type.types_name,
                # "variants": [
                # {
                #     "option1": colors[0],
                #     "option2": size[0]
                # },
                # {
                #     "option1": colors[1],
                #     "option2": size[1]
                # }
                # ],
                "variants": arr_varient,
                "options": [
                {
                    "name": "Color",
                    "values": [i.color for i in color_data]
                },
                {
                    "name": "Size",
                    "values": [i.size for i in size_data]
                }
                ]
            }
            })
            
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': i.api_token
            }
            conn.request("POST", "/admin/api/2022-07/products.json", payload, headers) 
            res = conn.getresponse()
            data = res.read()
            # print(data.decode("utf-8"))
            json_data = data.decode("utf-8")
            json_load = json.loads(json_data)
            json_product = json_load["product"]
            # print("////////",json_product['variants'])
            json_variants = json_product['variants'][0]
            print("////////",json_variants['id'])
            
            
            self.shopify_id = json_product['id']
            self.variant_id = json_variants['id']
           
            #----------------------------------Add Image------------------------------------------
            product_image = self.image.decode("utf-8")
            # print("UUUUUUUUUU",self.image)
            image_payload = json.dumps({
                "image": {
                    "attachment": product_image,
                    # "filename": ".jpeg"
                }
            })
            # print("IIIIIIIII",image_payload)
            conn.request("POST", "/admin/api/2022-07/products/"+ self.shopify_id +"/images.json", image_payload, headers)
            res_2 = conn.getresponse()
            image_data = res_2.read()
            # print(image_data.decode("utf-8"))
            json_image = image_data.decode("utf-8")
            
            #-----------------------GET IMAGE ID AND STORE TO FORM-------------------
            image_load = json.loads(json_image)
            image_details = image_load["image"]
            # print("IIIIIIIII",image_details['id'])
            
            self.image_id = image_details['id']

    def update_product(self):
        """update product data"""
        self.status = "Updated"
        color_data = self.env['color.product'].search([])
        size_data = self.env['size.product'].search([])
        
        color_details = self.varients_ids
        
        #this is a varients details color code
        colors = []
        color_data1 = [d for d in color_details[0].color_id]
        color_data2 = [d for d in color_details[1].color_id]
        for c1 in color_data1:
            colors.append(c1.color)
        for c2 in color_data2:
            colors.append(c2.color)
                    
        #this is a varients details size code
        size = []
        size_data1 = [d for d in color_details[0].product_size_id]
        size_data2 = [d for d in color_details[1].product_size_id]
        for s1 in size_data1:
            size.append(s1.size)
        for s2 in size_data2:
            size.append(s2.size)
        
        #update the products
        for i in self.store_name:
            conn = http.client.HTTPSConnection(i.store_name+".myshopify.com")
            payload = json.dumps({
            "product": {
                "id": self.shopify_id,
                "title": self.product_name.name,
                "body_html": self.description,
                "vendor": self.vendor,
                "product_type": self.product_type.types_name,
                "variants": [
                {
                    "option1": colors[0],
                    "option2": size[0]
                },
                {
                    "option1": colors[1],
                    "option2": size[1]
                }
                ],
                "options": [
                {
                    "name": "Color",
                    "values": [i.color for i in color_data]
                },
                {
                    "name": "Size",
                    "values": [i.size for i in size_data]
                }
                ]
            }
            })
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': i.api_token
            }
            conn.request("PUT", "/admin/api/2022-07/products/"+self.shopify_id+".json", payload, headers)
            res = conn.getresponse()
            data = res.read()
            # print(data.decode("utf-8"))

            #----------------------------------UPDATE IMAGE------------------------------------------
            product_image = self.image.decode("utf-8")
            # print("UUUUUUUUUU",self.image)
            image_payload = json.dumps({
                "image": {
                    "id": self.image_id,
                    "attachment": product_image,
                    # "filename": ".jpeg"
                }
            })
            conn.request("PUT", "/admin/api/2022-07/products/"+self.shopify_id+"/images/"+self.image_id+".json", image_payload, headers)
            res_2 = conn.getresponse()
            image_data = res_2.read()
            print("+++++++++++++++++",image_data.decode("utf-8"))
            
    def delete_product(self):
        """Delete Product"""
        self.status = "Deleted"
        for i in self.store_name:
            conn = http.client.HTTPSConnection(i.store_name+".myshopify.com")
            payload = ''
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': i.api_token
            }
            conn.request("DELETE", "/admin/api/2022-07/products/"+self.shopify_id+".json", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print("DDDDDDDDDDDDDDDeleted",data.decode("utf-8"))
            
    @api.onchange('store_name')
    def _onchange_(self):
        """Auto Change value"""
        for i in self.store_name:
            self.vendor = i.vendor_name.name
