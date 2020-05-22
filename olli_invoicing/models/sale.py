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
            'payment_method_id': 1,
            'invoice_ids': [invoice_id]
        })
        payment.create_payments()
        template_id = self.env.ref('account.email_template_edi_invoice')
        # template_id.send_mail(invoice_id, force_send=True)
        composer = self.env['mail.compose.message'].create({
            'composition_mode': 'comment',
        })
        invoice_send = self.env['account.invoice.send'].create({
            'is_email': True,
            'invoice_ids': [invoice_id],
            'composer_id': composer.id,
            'template_id': template_id
        })
        invoice_send._send_email()
        return invoice_id
