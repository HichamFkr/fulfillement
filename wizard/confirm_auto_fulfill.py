# -*- coding: utf-8 -*-
from audioop import reverse

from openerp import fields, models, api
import numpy as np


class sale_order_auto_fulfill(models.TransientModel):
    _name = 'sale_order.auto.fulfill'

    def _decesion_matrix(self, partners):
        def fill(row, n, begin, end):
            if n == 1:
                n = 1
            else:
                n = 0
            row[int(begin): int(end)] = n

            return row
        nbr_client = len(partners)
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


    @api.one
    def _fulfill(self, line):
        # line.ensure_one()
        qty = line.product_uom_qty * line.sla_line_min
        if type(qty) == "Float":
            line.qty_livre = int(qty) + 1
        else:
            line.qty_livre = qty
        self.env['sale.order.fulfill'].confirm_fulfillement()



    @api.one
    def auto_fulfillement(self):
        so_ids = self.env.context.get('active_ids')
        lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.state=='fulfillement')

        partners = []
        scores = []
        orders = []
        lines_sort_by_score_partner = []
        decesion_scores = []

        orders.append(lines.mapped('order_id'))
        scores.append(lines.mapped('fulfillement_score_partner'))
        partners.append(lines.mapped('order_id.partner_id'))

        for line in lines:
            lines_sort_by_score_partner.append(line)

        for s in scores:
            arr_scores = np.sort(np.array(list(dict.fromkeys(s))))[::-1] #convert list to numpy array

        # arr_scores =  np.sort(scores)
        # print arr_scores

        lines_sort_by_score_partner.sort(key=lambda l: l.fulfillement_score_partner, reverse=True)
        partners_sorted = []
        for l in lines_sort_by_score_partner:
            partners_sorted.append(l.order_partner_id)

        partners_sorted = list(dict.fromkeys(partners_sorted))
        partners_sorted.sort(key= lambda p:p.credit, reverse=True)

        #remove duplicate partners
        decesion_matrix = self._decesion_matrix(partners_sorted)
        decesion_scores = np.dot(decesion_matrix , arr_scores.T) #to determine highest scores
        # print decesion_matrix
        # print decesion_scores

        max_score = np.max(decesion_scores)
        index_max_score = np.argmax(decesion_scores)

        decesion_partners = decesion_matrix[index_max_score]

        final_decesion_partners = []

        for index, item in enumerate(decesion_partners, start=0):
            if item == 1.0:
                final_decesion_partners.append(partners_sorted[index])
        # print decesion_matrix
        # print decesion_scores
        # print decesion_partners
        # print final_decesion_partners
        #
        self._check_sla_order(final_decesion_partners)
        # for p in final_decesion_partners:
        #     print p

    @api.multi
    def _check_sla_line(self, line):
        # so_ids = self.env.context.get('active_ids')
        # lines = self.env['sale.order.line'].browse(so_ids).filtered(lambda line: line.state == 'fulfillement')
        if line.qty_livre >= (line.product_uom_qty * line.sla_line_min):
            return True

    @api.multi
    def _check_sla_order(self, partners):
        for r in self:
            count = 0
            for p in partners:
                slas = p.fulfillement_sla_ids
                for sla in slas:
                    if sla:
                        if sla.sla_id.fulfillement_sla_name == "Order percent":
                            orders = r.env['sale.order'].search([('partner_id', '=', p.id)])
                            for o in orders:
                                for l in o.mapped('order_line'):
                                    r._fulfill(l)
                                for l in o.mapped('order_line'):
                                    if r._check_sla_line(l) == True or l.state != 'fulfillement':
                                        count += 1
                                if count/o.nb_lines >= sla.value:
                                    return True
