from odoo import models, fields, api

class estate_property(models.Model):
    _name = 'estate.property'
    _description = 'estate.property'

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection( 
[('North','North'),('South','South'),('East','East'),('West','West')], 
        string="Garden Orientation")
    status = fields.Selection( 
[('New','New'),('Offer Received','Offer Received'),('Offer Granted','Offer Granted')], 
        string="Status", default="New")
    active = fields.Boolean("Active")
    partner_id = fields.Many2one("res.partner", string="Partner")
    partner_type = fields.Many2one("estate.property_type", string="Property Type")
    property_tags = fields.Many2many("estate.property_tags", string="Property Tags")