# -*- coding: utf-8 -*-


from openerp import models, fields, api

class fulfillement_sale_order_type(models.Model):
	_inherit = 'sale.order.type'

	fulfillement_score_so_type = fields.Integer("Score type de commande") #, compute='_get_score'
	fulfillement_so_type_coef = fields.Integer()
	fulfillement_so_is_eligible = fields.Boolean("Eligible", default=False, store=True)

