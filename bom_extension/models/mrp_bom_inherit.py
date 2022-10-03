from odoo import models, fields, api
""" Mrp Bom Inherit """

class mrp_bom_inherit(models.Model):
    _inherit = 'mrp.bom'
    
    state = fields.Selection(
        string='State',
        selection=[('In Development', 'In Development'), 
                   ('In Production', 'In Production')],
        default='In Development'
      )
    
    revision_ids  = fields.One2many('mrp.bom.revision','revision_id')
     
        
    def set_to_development(self):
       self.state = 'In Development'   