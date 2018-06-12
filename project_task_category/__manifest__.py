# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project Task Categories',
    'summary': 'Allow unique category for Tasks',
    'version': '11.0.1.0.0',
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'contributors': "Punt Sistemes",
    'license': 'AGPL-3',
    'category': 'Project Management',
    'website': 'https://www.elico-corp.com',
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/project_data.xml',
        'views/project_categ_view.xml',
        'views/project_task_view.xml',
    ],
    'installable': True,
}
