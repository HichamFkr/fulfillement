# -*- coding: utf-8 -*-
from openerp import models, fields, api


class fulfillement_enciente(models.Model):
    _name = 'fulfillement.enciente'
    enciente_id = fields.Many2one('res.partner.score', ondelete='set null')
    date_debut = fields.Integer(string="debut d'interval")
    date_fin = fields.Integer(string="fin d'interval")
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK(date_debut<=date_fin)',"intervale début doit être superieur à l'intervale fin"),]

class fulfillement_chiffre_affaire(models.Model):
    _name = 'fulfillement.chiffre.affaire'
    chiffre_affaire_id = fields.Many2one('res.partner.score', ondelete='set null')
    somme_debut = fields.Float('Somme début')
    somme_fin = fields.Float('Somme fin')
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK(somme_debut<=somme_fin)','Somme début doit être superieur à la somme fin'),]

class res_partner_score(models.Model):
    _name = 'res.partner.score'
    anciente = fields.Boolean(string='Anciente')
    coeff_enciente = fields.Float(string="Coeffecient")
    enciente_ids = fields.One2many('fulfillement.enciente','enciente_id', string="Configuration")

    chiffre_affaire = fields.Boolean(string="Chiffre d'affaire")
    coeff_chiffre_affaire = fields.Float(string="Coeffecient")
    chiffre_affaire_ids = fields.One2many('fulfillement.chiffre.affaire','chiffre_affaire_id', string="Configuration")

    potentiel = fields.Boolean(string="Potentiel")
    potentiel_id = fields.Many2one('fulfillement.potentiel','Potentiel', ondelete='set null')
    coeff_potentiel = fields.Float(string="Coeffecient")
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK((coeff_enciente + coeff_chiffre_affaire + coeff_potentiel)==1)','La somme des coefficient doit être égale à 1'),]


class sale_order_score(models.Model):
    _name = 'sale.order.score'

    type_cmd = fields.Boolean(string="Type de commande")
    coeff_type_cmd = fields.Float(string="Coefficient")
    type_cmd_ids = fields.Many2one('sale.order.type', 'Order Type', ondelete='set null')
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK(coeff_type_cmd<=1)','Le coefficient doit être inférieur ou égale à 1'),]







