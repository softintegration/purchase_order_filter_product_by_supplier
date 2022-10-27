# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        self.order_line = False
        return res

    @api.constrains('partner_id', 'order_line')
    def _check_order_line_products_supplier(self):
        """ Check that all the selected products have the supplier in their list of sellers"""
        if self.partner_id and self.order_line:
            for product in self.order_line.mapped('product_id'):
                if self.partner_id.id not in product.seller_ids.mapped("name").ids:
                    raise UserError(_("All the products must have the supplier in their list of sellers!"))
