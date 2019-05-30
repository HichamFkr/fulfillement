# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from passlib.tests.test_utils_handlers import dummy_handler_in_registry


class fulfillement_sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	fulfillement_is_eligible = fields.Boolean(default=False, compute="_is_eligible", store=True, string="Eligible")
	fulfillement_score_partner = fields.Integer(string="Score", compute="_get_score_partner")
	qty_livre = fields.Float(string="Quantité à livré")
	virtual_qty_available = fields.Float(string="Available qty", compute="_get_qty_available")
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
			r.sla_line_min = (r.order_partner_id.fulfillement_sla_ids.value)*100.0/ 100.0

	
	@api.depends('qty_livre', 'qty_available')
	def _get_qty_available(self):
		for r in self:
			r.virtual_qty_available = r.qty_available
		for r in self:
			r.virtual_qty_available = r.virtual_qty_available - r.qty_livre

	@api.depends('order_partner_id.credit')
	def _get_score_partner(self):
		for r in self:
			if (r.order_partner_id.credit >= 0.0 and r.order_partner_id.credit <= 1000.0):
				r.fulfillement_score_partner = 2
			elif (r.order_partner_id.credit > 1000.0 and r.order_partner_id.credit <= 2000.0):
				r.fulfillement_score_partner = 4
			else:
				r.fulfillement_score_partner = 5

	@api.depends('product_id', 'order_partner_id', 'order_type_id')
	def _is_eligible(self):
		self.env.invalidate_all()
		for r in self:
			if (r.product_id.fulfillement_is_eligible and r.order_type_id.fulfillement_so_is_eligible and r.order_partner_id.fulfillement_is_eligible):
				r.fulfillement_is_eligible = True