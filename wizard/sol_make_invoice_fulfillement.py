from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import workflow

class sol_fulfillement_make_invoice(osv.osv_memory):
    _inherit = "sale.order.line.make.invoice"

    _name = "sol.fulfillement.make.invoice"

    def make_invoices_fulfillement(self, cr, uid, ids, context=None):
        name_obj = context.get('active_model')

        if context is None: context = {}
        res = False
        invoices = {}
        inv_line_obj = self.pool.get('account.invoice.line')

        def make_invoice(order,lines):

            #return invoice's id

            inv = self._prepare_invoice(cr, uid, order, lines)
            inv_id = self.pool.get('account.invoice').create(cr, uid, inv)
            return inv_id

        sales_order_line_obj = self.pool.get('sale.order.line')
        sales_order_obj = self.pool.get('sale.order')

        dict_prod_inv = {}

        order_lines = sales_order_line_obj.browse(cr, uid, context.get('active_ids', []), context=context).lines_to_invoice()

        for line in order_lines:
            define_line = []
            define_line.append(line.order_id.id)
            define_line.append(line.product_id and line.product_id.id or False)
            define_line.append(line.lot_id)
            define_line.append(line.discount)
            define_line.append(line.tax_id)
            define_line.append(line.price_unit)

            if (not line.invoiced) and (line.state not in ('draft', 'cancel')):
                if line.product_id:
                    if str(define_line) in dict_prod_inv:
                        inv_l = inv_line_obj.browse(cr, uid, dict_prod_inv[str(define_line)])[0]
                        inv_line_obj.write(cr, uid, dict_prod_inv[str(define_line)], {'quantity':inv_l.quantity + line.qty_livre})
                        sales_order_line_obj.write(cr, uid, line.id, {'invoiced': True, 'invoice_lines': [(4, dict_prod_inv[str(define_line)])]})
                    else:
                        if not line.order_id in invoices:
                            invoices[line.order_id] = []
                        line_id = sales_order_line_obj.invoice_line_create(cr, uid, [line.id])
                        dict_prod_inv[str(define_line)] = line_id[0]
                        for lid in line_id:
                            invoices[line.order_id].append(lid)
                else:
                    if not line.order_id in invoices:
                        invoices[line.order_id] = []
                    line_id = sales_order_line_obj.invoice_line_create(cr, uid, [line.id])
                    for lid in line_id:
                        invoices[line.order_id].append(lid)
        for order, il in invoices.items():
            res = make_invoice(order, il)
            cr.execute('INSERT INTO sale_order_invoice_rel \
                                (order_id,invoice_id) values (%s,%s)', (order.id, res))
            sales_order_obj.invalidate_cache(cr, uid, ['invoice_ids'], [order.id], context=context)
            flag = True
            sales_order_obj.message_post(cr, uid, [order.id], body=_("Invoice created"), context=context)
            data_sale = sales_order_obj.browse(cr, uid, order.id, context=context)
            for line in data_sale.order_line:
                if not line.invoiced and line.state != 'cancel':
                    flag = False
                    break
            if flag:
                line.order_id.write({'state': 'progress'})
                workflow.trg_validate(uid, 'sale.order', order.id, 'all_lines', cr)
        if not invoices:
            raise osv.except_osv(_('Warning!'), _(
                'Invoice cannot be created for this Sales Order Line due to one of the following reasons:\n1.The state of this sales order line is either "draft" or "cancel"!\n2.The Sales Order Line is Invoiced!'))
        if context.get('open_invoices', False):
            return self.open_invoices(cr, uid, ids, res, context=context)
        return {'type': 'ir.actions.act_window_close'}

