# -*- coding: utf-8 -*-
from openerp import http

# class InsidjamStockFulfillement(http.Controller):
#     @http.route('/insidjam_stock_fulfillement/insidjam_stock_fulfillement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/insidjam_stock_fulfillement/insidjam_stock_fulfillement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('insidjam_stock_fulfillement.listing', {
#             'root': '/insidjam_stock_fulfillement/insidjam_stock_fulfillement',
#             'objects': http.request.env['insidjam_stock_fulfillement.insidjam_stock_fulfillement'].search([]),
#         })

#     @http.route('/insidjam_stock_fulfillement/insidjam_stock_fulfillement/objects/<model("insidjam_stock_fulfillement.insidjam_stock_fulfillement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('insidjam_stock_fulfillement.object', {
#             'object': obj
#         })