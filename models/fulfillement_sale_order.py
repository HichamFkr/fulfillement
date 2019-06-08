# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
import time

class fulfillement_sale_order(models.Model):
    _inherit = 'sale.order'

    def action_wait(self, cr, uid, ids, context=None):
        super(fulfillement_sale_order, self).action_wait(cr, uid, ids, context=context)
        line_obj = self.pool.get('sale.order.line')
        for o in self.browse(cr, uid, ids):
            line_obj.button_confirm(cr, uid, [x.id for x in o.order_line if
                                              x.state != 'cancel' and not x.fulfillement_is_eligible])
            line_obj.button_fulfill(cr, uid, [x.id for x in o.order_line if x.state != 'cancel' and x.fulfillement_is_eligible])