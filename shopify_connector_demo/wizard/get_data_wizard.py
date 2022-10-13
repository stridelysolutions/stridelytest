# -*- coding: utf-8 -*-
from odoo import fields,models 
import http.client
import json

class Getdatawizard(models.TransientModel):
    """Get Data Wizard"""
    _name = 'get.data.wizard'
    _description = 'Get data wizard'
    _rec_name = "store_id"
    

    store_id = fields.Many2one('account.access',string = "Store Name")

    
    def account_access_data(self):
        """Account access data"""
        context=self.env.context.get("active_id")
        print("!!!!!!!!!!!!!!1",context)
        data_get = self.env['home.dashbord'].browse(context)
        for data in self.store_id:
            store_name = data.store_name
            api_token = data.api_token   
            conn = http.client.HTTPSConnection(store_name+".myshopify.com")
            payload = ''
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': api_token
                }
            conn.request("GET", "/admin/oauth/access_scopes.json", payload, headers)
            res = conn.getresponse()
            data = res.read()
            # print(data.decode("utf-8"))
            
            json_data = data.decode("utf-8")
            json_load = json.loads(json_data)
            for i in json_load["access_scopes"]:
                print("+++++++",i["handle"])
                
            data_get.write({'output':json_data})

    def cancel(self):
        return False
