from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

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
        [('North', 'North'), ('South', 'South'),
         ('East', 'East'), ('West', 'West')],
        string="Garden Orientation"
    )
    total_area = fields.Integer(
        "Total Area (sqm)", compute="_compute_total_area")
    status = fields.Selection(
        [('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'),
         ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        string="Status", default="New"
    )
    active = fields.Boolean("Active", default=True)

    partner_id = fields.Many2one("res.partner", string="Partner")
    partner_type = fields.Many2one(
        "estate.property_type", string="Property Type")
    property_tags = fields.Many2many(
        "estate.property_tags", string="Property Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    user = fields.Many2one("res.users", string="Salesman",
                           default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer",
                            readonly=True, copy=False)

    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def button_sold(self):
        if "Cancelled" in self.mapped("status"):
            raise UserError("Cancelled properties cannot be sold.")
        return self.write({"status": "Sold"})

    def button_cancel(self):
        if "Sold" in self.mapped("status"):
            raise UserError("Sold properties cannot be Cancelled.")
        return self.write({"status": "Cancelled"})

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped(
                "price")) if prop.offer_ids else 0.0
