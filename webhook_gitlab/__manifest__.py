# Copyright 2018, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Webhook for Gitlab",
    "summary": "Controllers needed to notify actions with gitlab",
    "version": "15.0.1.0.1",
    "category": "Development",
    "author": "Jarsa Sistemas",
    "website": "https://git.vauxoo.com/jarsa/jarsa",
    "license": "LGPL-3",
    "depends": [
        "project",
    ],
    "data": [
        "views/message_templates.xml",
        "data/ir_config_parameter.xml",
        "data/project_tags_data.xml",
        "views/git_request_view.xml",
        "views/project_task_view.xml",
        "views/res_users_view.xml",
        "security/ir.model.access.csv",
    ],
    "external_dependencies": {
        "python": [
            "gitlab",
            "github",
        ],
    },
}
