# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_invoices(self):
        invoice_id = self._create_invoices().id
        _logger.info(_(invoice_id))
        return invoice_id
