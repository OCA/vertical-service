# -*- coding: utf-8 -*-
# © <YEAR(2015)>
# <Elico Corp, contributor: Eric Caudal, Alex Duan, Xie XiaoPeng(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Opportunity'
    )


class CrmLead(models.Model):
    _inherit = "crm.lead"

    resource_time_total = fields.Float(
        compute='_get_resource_time_total',
        string='Total Resource Time',
    )
    resource_cost_total = fields.Float(
        compute='_get_resource_cost_total',
        string='Total resource Cost',
    )

    @api.one
    def _get_resource_time_total(self):
        time_total = 0
        linked_brs = self.env['business.requirement'].search(
            [('lead_id', '=', self.id)])
        for br in linked_brs:
            if br.drop or br.state == 'cancel':
                continue
            time_total += br.resource_time_total
        self.resource_time_total = time_total

    @api.one
    def _get_resource_cost_total(self):
        cost_total = 0
        linked_brs = self.env['business.requirement'].search(
            [('lead_id', '=', self.id)])
        for br in linked_brs:
            if br.drop or br.state == 'cancel':
                continue
            cost_total += br.resource_cost_total
        self.resource_cost_total = cost_total
