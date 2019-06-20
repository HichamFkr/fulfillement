# -*- coding: utf-8 -*-
from audioop import reverse

from openerp import fields, models, api
import numpy as np


class sale_order_line_to_fulfill(models.TransientModel):
    _name = 'sale.order.fulfill'

    def _decesion_matrix(self, clients):
        def fill(row, n, begin, end):
            if n == 1:
                n = 1
            else:
                n = 0
            row[int(begin): int(end)] = n

            return row
        nbr_client = len(clients)
        rows = 2 ** nbr_client
        A = np.zeros((nbr_client, rows))
        iterations = 2
        for row in A:
            begin = 0
            end = rows / iterations
            step = end
            n = 1
            for _ in range(0, iterations):
                n *= -1
                row = fill(row, n, begin, end)

                begin = end
                end += step
            iterations *= 2
        # print "Decesion Matrix"
        # print A.T
        return A.T

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

    @api.one
    def auto_fulfillement(self):
        so_ids = self.env.context.get('active_ids')
        lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.state=='fulfillement')
        # for line in lines:
        #     qty = line.product_uom_qty * line.sla_line_min
        #     if type(qty) == "Float":
        #         line.qty_livre = int(qty) + 1
        #     else:
        #         line.qty_livre = qty
        #     print "==================="
        #     print str(line.qty_livre)
        #     self.confirm_fulfillement()
        partners = []
        scores = []
        orders = []
        lines_sort_by_score_partner = []
        decesion_scores = []

        for line in lines:
            orders.append(line.mapped('order_id'))
            scores.append(line.mapped('fulfillement_score_partner'))
            partners.append(line.mapped('order_id.partner_id'))
            lines_sort_by_score_partner.append(line)


        arr_scores = np.array(scores) #convert list to numpy array
        lines_sort_by_score_partner.sort(key=lambda l: l.fulfillement_score_partner, reverse=True)

        decesion_matrix = self._decesion_matrix(lines_sort_by_score_partner)
        decesion_scores = np.dot(decesion_matrix , arr_scores) #scores to determine highest scores

        max_score = np.max(decesion_scores)
        index_max_score = np.argmax(decesion_scores)
        decesion_partners = decesion_matrix[index_max_score]
        final_decesion_partners = []

        for index, item in enumerate(decesion_partners, start=0):
            if item == 1.0:
                final_decesion_partners.append(partners[index])

        # for p in final_decesion_partners:
        #     print o.order_id
        #     for o in p.mapped('order_id'):
        #