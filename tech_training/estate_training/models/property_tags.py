from odoo import models, fields, api


class estate_property_tags(models.Model):
    _name = 'estate.property_tags'
    _description = 'estate.property_tags'

    name = fields.Char("Property Tags", required=True)
    color = fields.Integer("Color Index")
