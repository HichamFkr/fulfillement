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

    @api.one
    @api.depends('order_partner_id.fulfillement_sla_ids', 'order_id.partner_id')
    def _get_html_tooltip_sla(self):
        partner = self.order_partner_id and self.order_partner_id.id or self.order_id.partner_id.id
        if partner:
            if partner:
                self._cr.execute(
                	"""select fulfillement_sla_name, value from fulfillement_sla INNER JOIN res_partner_sla ON (fulfillement_sla.id = res_partner_sla.sla_id) where res_partner_sla.partner_id =%s"""%(self.order_partner_id.id))
                res = self._cr.dictfetchall()
                if res:
                    if len(res) == 1:
                        self.html_tooltip_sla = """
                        <span class="ins-tooltip"> <i class="fa fa-info-circle fa-2x" style="color:#55b5e2"></i>

                        <span><strong>SLA : </strong> <span>"""+res[0]['fulfillement_sla_name']+"""</span>
                            <br />
                        <strong>Value : </strong><span> """+str(res[0]['value'])+""" %</span>
                            <br />
                        </span>
                        </span>
                     """
                    else:
                        self.html_tooltip_sla = """
                        <span class="ins-tooltip"> <i class="fa fa-info-circle fa-2x" style="color:#55b5e2"></i>

                        <span><strong>SLA : </strong> <span>"""+res[0]['fulfillement_sla_name']+"""</span>
                            <br />
                        <strong>Value : </strong><span> """+str(res[0]['value'])+""" %</span>
                            <br />
                        </span>
                        <span><strong>SLA : </strong> <span>"""+res[1]['fulfillement_sla_name']+"""</span>
                            <br />
                        <strong>Value : </strong><span> """+str(res[1]['value'])+""" %</span>
                            <br />
                        </span>
                        </span>
                     """
            else:
                self.html_tooltip_sla = ""

# @api.depends('order_partner_id.fulfillement_sla_ids', 'order_id.partner_id')
#     def _get_html_tooltip_sla(self):
#         for r in self:
#             SLAs = r.order_partner_id.fulfillement_sla_ids.search([('partner_id', '=', r.order_partner_id.id)])
#             lines=[]
#             orders=[]
#             for sla in SLAs:
#                 # print sla.partner_id
#                 # print sla.sla_id.fulfillement_sla_name
#                 # print sla.value
#                 if sla.sla_id.fulfillement_sla_name == 'Line percent':
#                     lines.append(sla)
#                 else:
#                     orders.append(sla)
#             for sla in lines, orders:
#                print sla.sla_id.fulfillement_sla_name