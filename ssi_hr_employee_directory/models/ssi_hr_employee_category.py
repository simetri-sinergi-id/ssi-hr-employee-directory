# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models


class EmployeeCategory(models.Model):
    _name = "ssi_hr.employee_category"
    _description = "Employee Category"
    _inherit = ["mail.thread"]

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(
        string="Tag Name",
        required=True,
    )
    color = fields.Integer(
        string="Color Index",
        default=_get_default_color,
    )

    # employee_ids = fields.Many2many(
    #    comodel_name='ssi_hr.employee',
    #    relation='employee_category_rel',
    #    column1='category_id',
    #    column2='emp_id',
    #    string='Employees'
    # )

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists !"),
    ]
