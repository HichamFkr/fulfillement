# -*- coding: utf-8 -*-
from passlib.tests.test_utils_handlers import dummy_handler_in_registry

from openerp import models, fields, api
from datetime import datetime

class fulfillement_partner(models.Model):
    _inherit = 'res.partner'

    fulfillement_is_eligible = fields.Boolean("Eligible", default=False, store=True)
    fulfillement_sla_ids = fields.One2many('res.partner.sla', 'partner_id', string="Regles de service")
    start_date = fields.Date(default=fields.Date.today)
    potentiel_id = fields.Many2one('fulfillement.potentiel', ondelete='set null', string="Potentiel")
    score = fields.Float(default = 0.0, compute='_get_score')

    @api.one
    def _get_score(self):
        score = self.env['res.partner.score'].browse(7).calcule_score(self)[0]
        self.score = score