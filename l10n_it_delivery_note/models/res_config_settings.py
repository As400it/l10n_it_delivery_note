# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import _, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_use_advanced_delivery_notes = fields.Boolean(
        string=_("Use the advanced delivery notes behaviour"),
        implied_group='l10n_it_delivery_note.'
                      'use_advanced_delivery_notes')

    draft_delivery_note_invoicing_notify = fields.Boolean(
        related='company_id.draft_delivery_note_invoicing_notify',
        readonly=False)
