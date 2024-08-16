from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.property.offer'

    price = fields.Float("Price", required=True)
    validity = fields.Integer("Validity (7 days)", default=7)

    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property_type", string="Property Type", store=True
    )

    date_deadline = fields.Date(string="Deadline")
