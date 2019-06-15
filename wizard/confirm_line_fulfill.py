# -*- coding: utf-8 -*-

from openerp import fields, models, api

class sale_order_line_to_fulfill(models.TransientModel):
    _name = 'sale.order.fulfill'

    @api.multi
    def confirm_fulfillement(self):
        so_ids = self.env.context.get('active_ids')
        lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.qty_livre>0 and line.state=='fulfillement')
        for line in lines:
            if line.product_uom_qty > line.qty_livre:
                #TODO : créer une ligne avec la diff
                data = {
                    'product_uom_qty':line.product_uom_qty - line.qty_livre,
                    'qty_livre':0.0,
                    'state': 'fulfillement'
                }
                new_line_id = line.copy(data)
        lines.write({'state':'confirmed', 'fulfillement_is_eligible':False})

    @api.multi
    def auto_fulfillement(self):
        so_ids = self.env.context.get('active_ids')
        lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.state=='fulfillement')
        for line in lines:
            qty = int(line.product_uom_qty * line.sla_line_min)
            line.qty_livre = qty + 1
            print "==================="
            print str(line.qty_livre)
            self.confirm_fulfillement()
