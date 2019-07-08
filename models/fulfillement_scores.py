# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime

class fulfillement_enciente(models.Model):
    _name = 'fulfillement.enciente'
    enciente_id = fields.Many2one('res.partner.score', ondelete='set null')
    date_debut = fields.Integer(string="debut d'interval")
    date_fin = fields.Integer(string="fin d'interval")
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK(date_debut<=date_fin)',"intervale début doit être superieur à l'intervale fin"),]

    def get_period(self, arg_date):
        period = datetime.today() - datetime.strptime(arg_date, '%Y-%M-%d')
        return round(period.days / 365)

    def calcul_score_anceinte(self, date):
        period = self.get_period(date)
        rules = sorted(self.search_read([],['date_fin', 'note']),key= lambda k:k['date_fin'])
        for rule in rules:
            if period <= rule['date_fin']:
                return rule['note']
        return 0.0



class fulfillement_chiffre_affaire(models.Model):
    _name = 'fulfillement.chiffre.affaire'
    chiffre_affaire_id = fields.Many2one('res.partner.score', ondelete='set null')
    somme_debut = fields.Float('Somme début')
    somme_fin = fields.Float('Somme fin')
    note = fields.Float(string="Note")

    _sql_constraints = [('check_value', 'CHECK(somme_debut<=somme_fin)','Somme début doit être superieur à la somme fin'),]

    def get_score_credit(self, credit):
        rules = sorted(self.search_read([],['somme_fin', 'note']), key= lambda k:k['somme_fin'])
        for rule in rules:
            if credit <= rule['somme_fin']:
                return rule['note']
        return 0.0


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

    @api.one
    def calcule_score(self, partner):
        score = 0.0
        if self.anciente:
            score += self.coeff_enciente * self.env['fulfillement.enciente'].calcul_score_anceinte(partner.start_date)

        if self.chiffre_affaire:
            score += self.coeff_chiffre_affaire * self.env['fulfillement.chiffre.affaire'].get_score_credit(partner.credit)

        if self.potentiel:
            score += self.coeff_potentiel * partner.potentiel_id.fulfillement_potentiel_value
        return score












class sale_order_age_score(models.Model):
    _name = "sale.order.age.score"
    age_id = fields.Many2one('sale.order.score', ondelete='set null')
    jour_debut = fields.Float('Jour début')
    jour_fin = fields.Float('Jour fin')
    note = fields.Float(string="Note")

class sale_order_score(models.Model):
    _name = 'sale.order.score'

    type_cmd = fields.Boolean(string="Type de commande")
    coeff_type_cmd = fields.Float(string="Coefficient")
    type_cmd_ids = fields.Many2one('sale.order.type', 'Order Type', ondelete='set null')
    note = fields.Float(string="Note")

    age_cmd = fields.Boolean(string="Age de la commande")
    coeff_age_cmd = fields.Float(string="Coeffecient")
    age_ids = fields.One2many('sale.order.age.score', 'age_id', string="Configuration")

    _sql_constraints = [('check_value', 'CHECK(coeff_type_cmd<=1)','Le coefficient doit être inférieur ou égale à 1'),]







