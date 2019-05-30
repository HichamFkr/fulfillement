# -*- coding: utf-8 -*-


from openerp import models, fields, api

class res_partner_sla(models.Model):
    _name = 'res.partner.sla'

    partner_id = fields.Many2one('res.partner', ondelete='set null', string="Partner")
    sla_id = fields.Many2one('fulfillement.sla', ondelete='set null', string="SLA")
    value = fields.Float(string="Value")

    _sql_constraints = [('name_uniq', 'unique(partner_id,sla_id)','You cant choose an SLA more than once!'),
                        ('check_value', 'CHECK(value<=100)','value must be <= 100!'),]
