# -*- coding: utf-8 -*-
from passlib.tests.test_utils_handlers import dummy_handler_in_registry

from openerp import models, fields, api
from datetime import datetime

class fulfillement_partner(models.Model):
    _inherit = 'res.partner'

    fulfillement_is_eligible = fields.Boolean("Eligible", default=False, store=True)
    fulfillement_score_anciente = fields.Integer("Score Anciente", compute='_get_score_anciente')
    fulfillement_score_chiffre_affaire = fields.Integer("Score Chiffre d'affaire", compute='_get_score_chiffre_affaire')
    fulfillement_score_partner = fields.Integer("Score", store=True) #, compute='_get_score_partner'
    fulfillement_partner_coef = fields.Integer()
    # fulfillement_sla = fields.Many2many("fulfillement.sla", string="SLAs")
    fulfillement_sla_ids = fields.One2many('res.partner.sla', 'partner_id', string="Regles de service")
    start_date = fields.Date(default=fields.Date.today)

    @api.depends('start_date')
    def _get_score_anciente(self):
        for r in self:
            if not (r.start_date):
                print("====")
            else:
                start = fields.Datetime.from_string(r.start_date)
                end = fields.Datetime.from_string(datetime.today())
                duration = (end - start).days

                if(duration>0 and duration<=1440):
                    r.fulfillement_score_anciente = 1
                elif(duration>1440 and duration<=2880):
                    r.fulfillement_score_anciente = 2
                else:
                    r.fulfillement_score_anciente = 3



    @api.multi
    def _get_score_chiffre_affaire(self):
        for r in self:
            if(r.credit >= 0 and r.credit <= 1000):
                r.score = 2
            elif(r.credit > 1000 and r.credit <= 2000):
                r.score = 4
            else:
                r.score = 5