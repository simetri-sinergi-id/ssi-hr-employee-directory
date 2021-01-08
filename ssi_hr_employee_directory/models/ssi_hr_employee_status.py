# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EmployeeStatus(models.Model):
    _name = "ssi_hr.employee_status"
    _description = "Employee Status"
    _inherit = ["mail.thread"]

    name = fields.Char(
        string="Employee Status",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        default=lambda self: self.env.company,
    )

    # employee_ids = fields.Many2many(
    #    comodel_name='ssi_hr.employee',
    #    relation='employee_category_rel',
    #    column1='category_id',
    #    column2='emp_id',
    #    string='Employees'
    # )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "The name of the employee status must be unique in company!",
        ),
    ]
