# Copyright (c) 2019, Link IT Europe Srl (http://www.linkgroup.it/)
# @author: Matteo Bilotta <mbilotta@linkgroup.it>

import datetime

from odoo import api, fields, models


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _name = 'stock.delivery.note.create.wizard'
    _inherit = 'stock.delivery.note.base.wizard'
    _description = "Delivery note creator"

    def _default_date(self):
        return datetime.date.today()

    def _default_type(self):
        return self.env['stock.delivery.note.type'].search([], limit=1)

    partner_shipping_id = fields.Many2one('res.partner', required=True)

    date = fields.Date(default=_default_date)
    type_id = fields.Many2one('stock.delivery.note.type', default=_default_type, required=True)

    @api.model
    def check_compliance(self, pickings):
        super().check_compliance(pickings)

        self._check_delivery_notes(pickings)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.partner_shipping_id = self.partner_id

    def confirm(self):
        self.check_compliance(self.selected_picking_ids)

        delivery_note = self.env['stock.delivery.note'].create({
            'partner_sender_id': self.partner_sender_id.id,
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'type_id': self.type_id.id,
            'date': self.date,

            'delivery_method_id': self.partner_id.property_delivery_carrier_id.id,
            'transport_condition_id': self.partner_id.transport_condition_id.id,
            'goods_appearance_id': self.partner_id.goods_appearance_id.id,
            'transport_reason_id': self.partner_id.transport_reason_id.id,
            'transport_method_id': self.partner_id.transport_method_id.id
        })

        self.selected_picking_ids.write({'delivery_note_id': delivery_note.id})
