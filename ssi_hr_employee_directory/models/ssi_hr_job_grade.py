# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrJobGrade(models.Model):
    _name = "ssi_hr.job_grade"
    _description = "Job Grade"
    _inherit = ["mail.thread"]

    name = fields.Char(
        string="Job Grade",
        required=True,
        translate=True,
    )
    job_grade_category_id = fields.Many2one(
        string="Job Grade Category",
        comodel_name="ssi_hr.job_grade_category",
        required=False,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        default=lambda self: self.env.company,
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "The name of the job grade must be unique in company!",
        ),
    ]
