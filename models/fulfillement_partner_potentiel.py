# -*- coding: utf-8 -*-


from openerp import models, fields, api

class fulfillement_partner_potentiel(models.Model):
    _name = 'fulfillement.potentiel'

    fulfillement_potentiel_name = fields.Char(string="Name", required=True)
    fulfillement_potentiel_description = fields.Text(string="Description")
    fulfillement_potentiel_value = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', ondelete='set null', string="Client")