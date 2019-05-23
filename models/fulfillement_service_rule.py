# -*- coding: utf-8 -*-


from openerp import models, fields, api

class fulfillement_service_rule(models.Model):
    _name = 'fulfillement.sla'

    fulfillement_sla_name = fields.Char(string="Name", required=True)
    fulfillement_sla_description = fields.Text(string="Description")
    fulfillement_sla_value = fields.Integer(string="Pourcentage de remplissage")
    # is_active = fields.Boolean(default=False, string="Active")
    fulfillement_sla_ids = fields.One2many('res.partner.sla', 'sla_id')
    #partner_ids = fields.Many2many('res.partner', string='Clients')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, "%s" % (record.fulfillement_sla_name)))
        return res



