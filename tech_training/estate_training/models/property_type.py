from odoo import models, fields, api


class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'estate.property.type'
    _sql_constraints = [
        ("check_name", "Unique(name)", " The name must be unique"),
    ]

    name = fields.Char("Property Type", required=True)
    sequence = fields.Integer("Sequence", default=10)

    property_ids = fields.One2many(
        "estate.property", "partner_type", string="Properties")

    offer_counts = fields.Integer(
        string='Number of Offers', compute='_compute_offer_count')
    offer_ids = fields.Many2many(
        "estate.property.offer", string="Offers", compute="_compute_offer_count")

    def _compute_offer_count(self):
        data = self.env['estate.property.offer'].read_group(
            [('property_id.status', '!=', 'Canceled'),
             ('property_type_id', '!=', False)],
            ['ids:array_agg(id)', 'property_type_id'],
            ['property_type_id'],
        )
        mapped_count = {d['property_type_id'][0]
            : d['property_type_id_count'] for d in data}
        mapped_ids = {d['property_type_id'][0]: d['ids'] for d in data}
        for prop_type in self:
            prop_type.offer_counts = mapped_count.get(prop_type.id, 0)
            prop_type.offer_ids = mapped_ids.get(prop_type.id, [])

    def action_view_offers(self):
        res = self.env.ref("estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res
