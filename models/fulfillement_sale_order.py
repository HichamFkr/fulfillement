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

class sla_tool_tip(models.Model):
    _inherit = 'sale.order.line'

    html_tooltip_sla = fields.Text(string="SLA", compute="_get_html_tooltip_sla")
    qty_livre = fields.Float(string="Quantité à livré", default=lambda self: self._set_qte_livre())

    _sql_constraints = [('check_value', 'CHECK(qty_livre>=sla_line_min * product_uom_qty)',"Erreur"),]

    @api.model
    def _set_qte_livre(self):
        qty = self.product_uom_qty  + (self.product_uom_qty * self.sla_line_min)
        return qty



    @api.depends('order_partner_id.fulfillement_sla_ids', 'order_id.partner_id')
    def _get_html_tooltip_sla(self):
        for line in self:
            slas = line.order_partner_id.fulfillement_sla_ids
            html_tooltip_sla = ""
            for sla in slas:
                html_tooltip_sla += """
                        <span><strong>SLA : </strong><span>""" + sla.sla_id.fulfillement_sla_name + """</span><br />
                        <strong>Value : </strong><span> """ + str(sla.value) + """ %</span><br />
                 """
            line.html_tooltip_sla = """
                    <span class="ins-tooltip"><i class="fa fa-info-circle fa-2x" style="color:#55b5e2"></i>
                    """ + html_tooltip_sla + """</span>"""
