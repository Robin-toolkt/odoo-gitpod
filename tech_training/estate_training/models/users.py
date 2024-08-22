from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "user", string="Properties",
        domain=[("status", "in", ("New", "Offer Received"))]
    )
