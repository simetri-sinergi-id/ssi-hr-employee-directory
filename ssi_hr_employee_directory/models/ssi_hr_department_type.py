# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DepartmentType(models.Model):
    _name = "ssi_hr.department_type"
    _description = "Department Type"
    _inherit = ["mail.thread"]
    _order = "sequence, id"

    name = fields.Char(
        string="Department Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
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
    department_ids = fields.One2many(
        comodel_name="ssi_hr.department",
        inverse_name="department_type_id",
        string="Departments",
        readonly=True,
    )
    note = fields.Text(
        string="Note",
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "The name of the department type must be unique in company!",
        ),
    ]
