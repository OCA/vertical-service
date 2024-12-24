from odoo import models


class ModelName(models.Model):
    _inherit = "project.project"

    def attachment_tree_view(self):
        attachment_action = self.env.ref("base.action_attachment")
        action = attachment_action.read()[0]
        action["domain"] = str(
            [
                "|",
                "&",
                ("res_model", "=", "project.project"),
                ("res_id", "in", self.ids),
                "&",
                ("res_model", "=", "project.task"),
                ("res_id", "in", self.task_ids.ids),
            ]
        )
        action["context"] = "{'default_res_model': '%s','default_res_id': %d}" % (
            self._name,
            self.id,
        )
        return action
