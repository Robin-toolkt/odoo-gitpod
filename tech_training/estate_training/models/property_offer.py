from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate.property.offer'
    _order = 'price desc'

    price = fields.Float("Price", required=True)
    validity = fields.Integer("Validity (days)", default=7)

    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.partner_type", string="Property Type", store=True
    )

    date_deadline = fields.Date(
        string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def button_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer is already been accepted")
        self.write(
            {
                "state": "accepted",
            }
        )
        other_offers = self.property_id.offer_ids.filtered(
            lambda offer: offer != self)
        other_offers.write({"state": "refused"})
        return self.mapped("property_id").write(
            {
                "status": "Offer Accepted",
                "selling_price": self.price,
                "buyer": self.partner_id.id,
            }
        )

    def button_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            prop.status = "Offer Received"
        return super().create(vals)
