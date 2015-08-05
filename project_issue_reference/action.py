# coding: utf-8
##############################################################################
#
#    Copyright (C) 2015-TODAY Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api


# generated by [str(ord(x)) for x in 'project_issue_reference']
UNIQUE_ACTION_ID = (
    11211411110610199116951051151151171019511410110210111410111099101)


class IrValues(models.Model):
    _inherit = 'ir.values'

    @api.model
    def get_actions(self, action_slot, model, res_id=False):
        """ Add an action to all Model objects of the ERP """
        res = super(IrValues, self).get_actions(
            action_slot, model, res_id=res_id)
        available_models = [
            x[0]for x in self.env['project.issue']._authorised_models()
            if x[0] != 'project.issue']
        if action_slot == 'client_action_multi' and model in available_models:
            action = self.set_issue_action(model, res_id=res_id)
            value = (UNIQUE_ACTION_ID, 'project_issue_reference', action)
            res.insert(0, value)
        return res

    @api.model
    def set_issue_action(self, model, res_id=False):
        action_id = self.env.ref(
            'project_issue_reference.project_issue_from_anywhere').id
        return {
            'id': action_id,
            'name': 'Report an issue',
            'res_model': u'project.issue',
            'src_model': model,
            'type': u'ir.actions.act_window',
            'target': 'current',
        }
