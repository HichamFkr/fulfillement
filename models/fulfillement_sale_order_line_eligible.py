# -*- coding: utf-8 -*-
from openerp import models, fields, api
from passlib.tests.test_utils_handlers import dummy_handler_in_registry


class fulfillement_sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	fulfillement_is_eligible = fields.Boolean(default=False, compute="_is_eligible", store=True, string="Eligible")

	@api.depends('product_id','product_id','order_partner_id','order_type_id')
	def _is_eligible(self):
		for r in self:
			print(" PARTNER ",r.order_partner_id.fulfillement_is_eligible)
			print(" PROD ",str(r.product_id.fulfillement_is_eligible))
			print(" TYPE ",str(r.order_type_id.fulfillement_so_is_eligible))
			if(r.product_id.fulfillement_is_eligible and r.order_type_id.fulfillement_so_is_eligible):
				r.fulfillement_is_eligible = True
				print(" ELIGIBLE ")
			else:
				print(" NOT ELIGIBLE ")


class fulfillement_sale_order_line_eligible(models.Model):
	_name = 'fulfillement.sol.eligible'

	product_qty_fulfilled = fields.Float()
	fulfillement_score_age = fields.Integer() #compute='_get_score_age'
	fulfillement_score_cmd = fields.Integer() #compute='_get_score_cmd'
	fulfillement_score_prod = fields.Integer() #compute='_get_score_prod'
	fulfillement_score_partner = fields.Integer() #compute='_get_score_partner'
	fulfillement_score_sale_order_line = fields.Float(string="Score line", store=True) #, compute='_get_score_line'



