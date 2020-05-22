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
        template = self.env.ref('account.email_template_edi_invoice')
        # template_id.send_mail(invoice_id, force_send=True)
        composer = self.env['mail.compose.message'].create({
            'composition_mode': 'comment',
        })
        invoice_send = self.env['account.invoice.send'].create({
            'is_email': True,
            'invoice_ids': [invoice_id],
            'composer_id': composer.id,
            'template_id': template.id
        })
        lang = get_lang(self.env)
        ctx = dict(
            default_model='account.move',
            default_res_id=invoice_id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        invoice_send = invoice_send.with_context(ctx)
        invoice_send.send_and_print_action()
        return invoice_id
