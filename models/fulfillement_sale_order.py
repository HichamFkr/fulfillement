# -*- coding: utf-8 -*-


from openerp import models, fields, api

class fulfillement_sale_order(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    # def action_confirm(self):
    #     res = {}
    #     res = super(SaleOrder, self).action_confirm()
    #     return res