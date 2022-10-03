from odoo import models, fields, api
""" Mrp Bom Revision Wizard """

class mrp_bom_revision_wizard(models.Model):
    _name = 'mrp.bom.revision.wizard'

   
    bil_of_material = fields.Many2one('mrp.bom',string= "Bil Of Material",readonly=True , default=lambda self: self.env['mrp.bom'].search([('id','=',self.env.context.get('active_id'))]))
    no = fields.Integer(string = "Revision") 
    revision_description = fields.Text(string = 'Revision Description ')
    current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.uid)
    
    
    def create_data(self):
        context = self.env.context.get('active_id')
        self.env['mrp.bom.revision'].create({
            'no' : self.no,
            'revision_id':context,
            'modification_name':self.revision_description,
            'author':self.current_user.id
            })  
        search = self.env['mrp.bom'].search([('id','=',context)])
        search.write({
            'state':'In Production',
        }
        )
        
    
            

