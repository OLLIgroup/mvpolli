# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_invoices(self):
        return _create_invoices()
