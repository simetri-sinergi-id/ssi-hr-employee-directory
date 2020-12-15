# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrJobGradeCategory(models.Model):
    _name = "ssi_hr.job_grade_category"
    _description = "Job Grade Category"
    _inherit = ["mail.thread"]

    name = fields.Char(
        string="Job Grade Category",
        required=True,
        translate=True,
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
    job_grade_category_ids = fields.One2many(
        comodel_name="ssi_hr.job_grade",
        inverse_name="job_grade_category_id",
        string="Job Grade Category",
        readonly=True,
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "The name of the job grade category must be unique in company!",
        ),
    ]
