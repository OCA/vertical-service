===============================
Sale project reimbursement cost
===============================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:d39dbad9cb876d5f5a2aca0705081cb50c6f35342159a5d8a58ea55cd5a2cc26
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fproject-lightgray.png?logo=github
    :target: https://github.com/OCA/project/tree/17.0/sale_project_reimbursement_cost
    :alt: OCA/project
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/project-17-0/project-17-0-sale_project_reimbursement_cost
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/project&target_branch=17.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module allows the display of provisions and reimbursement costs in
the ``Project Updates`` dashboard.

**Table of contents**

.. contents::
   :local:

Use Cases / Context
===================

In businesses, especially those in services or consulting, where
expenses may be incurred on behalf of a client but later need to be
reimbursed by the client, Odoo’s functionality for
``Re-Invoice Expenses`` products (without using the hr_expenses module)
lacks visibility of this information in the project dashboard.

With this module, two sections are added to the project dashboard:

- **Provisions**: Values invoiced to the client in advance to cover any
  necessary expenses. This section displays the analytic entries
  generated from customer invoices for specific products.
- **Reimbursements cost:** Values generated from vendor bills that need
  to be charged to the client. Using Odoo’s functionality, these are the
  sales order lines automatically created from a vendor bill when the
  product is configured as ``Re-Invoice Expenses``.

Configuration
=============

**To automatically create a project from a sale order:**

- Go to ``Sales > Products > Products``.
- Create a new product with the following options:

  - Product Type: Service
  - Invoicing Policy: ``Prepaid/Fixed Price``.
  - Create on Order: Set an option other than ``Nothing``.

**For Provisions:**

- Go to ``Sales > Products > Products``.
- Create a new product of type Service.

**For Reimbursement:**

- Go to ``Sales > Products > Products``.
- Create a new product with the following options:

  - ``Product Type``: Service
  - Invoicing Policy: ``Based on Delivered Quantity (Manual)``.
  - ``Re-Invoice Expenses``: At cost or Sales price
  - Fill in the ``Provision Product`` field created in the previous
    step.

Usage
=====

**To generate a new project from a sale order**:

- Go to ``Sales > Orders > Quotations``.
- Create a new sales order and select the first product configured.
- Add a second line with the second configured product for
  ``Provisions``.
- Confirm the sales order.
- Generated the invoice

**To generate reimbursement costs**:

- Go to ``Invoicing > Vendors > Bills``.
- Create a new bill and select the third product configured for
  ``Reimbursement``.
- In the invoice line, set the analytic distribution with the analytic
  account for the project.
- Confirm the bill, and a new line will be added to the sale order with
  the reimbursement cost.
- While the provision has a remaining amount, a new line will be added
  to the sale order with the product for Provisions, but with a negative
  quantity.

**Project status dashboard**:

- Go to ``Project > Projects``.
- Search for the respective project.
- In the Kanban view, click the top-right icon to display project
  settings, then click ``Reporting / Project Updates``.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/project/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/project/issues/new?body=module:%20sale_project_reimbursement_cost%0Aversion:%2017.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Tecnativa

Contributors
------------

- `Tecnativa <https://www.tecnativa.com>`__:

  - Pedro M. Baeza
  - Carlos López

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/project <https://github.com/OCA/project/tree/17.0/sale_project_reimbursement_cost>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
