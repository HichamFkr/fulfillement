# -*- coding: utf-8 -*-
from openerp import models, fields
from passlib.tests.test_utils_handlers import dummy_handler_in_registry


class fulfillement_product(models.Model):
	_inherit = 'product.template'

	fulfillement_score_product = fields.Integer("Score type de commande") #, compute='_get_score'
	fulfillement_is_eligible = fields.Boolean("Eligible", default=False, store=True)
	fulfillement_partner_coef = fields.Integer()

