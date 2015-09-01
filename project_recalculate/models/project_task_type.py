# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    include_in_recalculate = fields.Boolean(
        string="Include in project recalculate", default=True,
        help="If you mark this check, tasks that are in this stage will be "
             "selectable for recalculating their dates when user click on "
             "'Recalculate project' button.")
