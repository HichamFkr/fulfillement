# -*- coding: utf-8 -*-

from openerp import fields, models, api

class confirm_line_fulfill(models.TransientModel):
    _name = 'sale.order.fulfill'

    def _default_line(self):
    	return self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        # return self.env['sale.order.line'].browse(self.env.context.get('active_ids'))

    line_id = fields.Many2one('sale.order.line', default=_default_line)



    @api.multi
    def confirm_fulfillement(self):
        print str(self.line_id.state)
        print str(self.line_id.product_qty)
        self.line_id.state = 'confirmed'
        self.line_id.product_qty = self.line_id.qty_livre

        # self.state = 'confirmed'
        # for r in self:
        #     if r.line_ids:
        #         for line in r.line_ids:
        #             print str(line.product_qty)
        #             # line.state = 'confirmed'

        # order_obj = self.pool.get('sale.order')
        cr = self._cr
        uid = self._uid
        print "======================"+str(self.line_id.order_id.code)
        orders = self.env['sale.order'].search(['code', '=', self.line_id.order_id.code])
        for o in orders:
            if o.order_line.order_id == self.order_id:
                    o.order_line.write({'product_qty': self.qty_livre})
        # line_ids = order_obj.search(['order_line', = , self.id])

        # order_obj.write(cr, ui, self.order_id , {self.})
