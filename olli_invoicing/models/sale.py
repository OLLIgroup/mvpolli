# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_invoices(self):
        invoice_id = self._create_invoices().id
        self.env['account.move'].search([('id','=',invoice_id)]).action_post()
        payment = self.env['account.payment.register'].create({
            'journal_id': 1,
            'payment_method_id': "Manual",
            'invoice_ids': [invoice_id]
        })
        payment.create_payments()
        return invoice_id
