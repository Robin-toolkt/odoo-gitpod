from odoo import models, fields, api

class estate_property_type(models.Model):
    _name = 'estate.property_type'
    _description = 'estate.property_type'
    
    name = fields.Char("Property Type", required=True)