# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from passlib.tests.test_utils_handlers import dummy_handler_in_registry


class fulfillement_sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	fulfillement_is_eligible = fields.Boolean(default=False, compute="_is_eligible", store=True, string="Eligible")
	fulfillement_score_partner = fields.Float(string="Score", related='order_partner_id.score')
	virtual_qty_available = fields.Float(string="Available qty", related="product_id.virtual_available")
	# virtual_qty_available = fields.Float(string="Available qty", compute="_get_qty_available")
	sla_line_min = fields.Float(string="Minimum Line Percent (%)", compute="_get_min_line")
	state = fields.Selection(selection_add=[('fulfillement', 'Fulfillement')])


	@api.constrains('qty_livre', 'product_qty')
	def _check_qty_livre(self):
		for record in self:
			if record.qty_livre < 0.0:
				raise ValidationError("Quantity must be positive ! \n Quantity : %s" % record.qty_livre)
			elif record.qty_livre > record.product_qty:
				raise ValidationError("Delivered quantity must be inferior than orde quantity \n Quantity : %s" % record.qty_livre)

	@api.depends('order_partner_id')
	def _get_min_line(self):
		for r in self:
			slas = r.order_partner_id.fulfillement_sla_ids
			for sla in slas:
				if sla.sla_id.fulfillement_sla_name == "Line percent":
					r.sla_line_min = sla.value / 100.0
				# else:
				# 	r.sla_line_min = 1.0




	@api.depends('product_id', 'order_partner_id', 'order_type_id')
	def _is_eligible(self):
		for r in self:
			if (r.product_id.fulfillement_is_eligible and r.order_type_id.fulfillement_so_is_eligible and r.order_partner_id.fulfillement_is_eligible):
				r.fulfillement_is_eligible = True




	def button_fulfill(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'fulfillement'})


