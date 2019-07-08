# -*- coding: utf-8 -*-
from audioop import reverse

from openerp import fields, models, api
import numpy as np


class sale_order_line_to_fulfill(models.TransientModel):
    _name = 'sale.order.fulfill'



    @api.multi
    def confirm_fulfillement(self):
        so_ids = self.env.context.get('active_ids')
        lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.qty_livre > 0 and line.state=='fulfillement')
        for line in lines:
            # if line.product_id.qty_available :
            if line.product_uom_qty > line.qty_livre:
                #TODO : créer une ligne avec la diff
                data = {
                    'product_uom_qty':line.product_uom_qty - line.qty_livre,
                    'qty_livre':0.0,
                    'state': 'fulfillement'
                }
                # prod_data = {
                #     'qty_available': line.product_id.qty_available - line.qty_livre
                # }
                new_line_id = line.copy(data)
        lines.write({'state':'confirmed', 'fulfillement_is_eligible':False})
        # lines.order_partner_id.write(prod_data)

