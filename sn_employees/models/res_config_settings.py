# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    # TODO:: revoir get et set
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Company Working Hours',
        related='company_id.resource_calendar_id', readonly=False)