# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Department(models.Model):
    _name = "ssi_hr.department"
    _description = "Department"
    _inherit = ["mail.thread"]
    _order = "name"
    _rec_name = "complete_name"

    name = fields.Char(
        string="Department Name",
        required=True,
    )
    complete_name = fields.Char(
        string="Complete Name",
        compute="_compute_complete_name",
        store=True,
    )
    department_type_id = fields.Many2one(
        comodel_name="ssi_hr.department_type",
        string="Department Type",
        index=True,
        # domain="['|', ('company_id', '=', False),
        # ('company_id', '=', company_id)]",
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
    parent_id = fields.Many2one(
        comodel_name="ssi_hr.department",
        string="Parent Department",
        index=True,
        # domain="['|', ('company_id', '=', False),
        # ('company_id', '=', company_id)]",
    )
    child_ids = fields.One2many(
        comodel_name="ssi_hr.department",
        inverse_name="parent_id",
        string="Child Departments",
    )
    manager_id = fields.Many2one(
        comodel_name="ssi_hr.employee",
        string="Manager",
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    member_ids = fields.One2many(
        comodel_name="ssi_hr.employee",
        inverse_name="department_id",
        string="Members",
        readonly=True,
    )
    jobs_ids = fields.One2many(
        comodel_name="ssi_hr.job_position",
        inverse_name="department_id",
        string="Jobs",
        readonly=True,
    )
    real_manager_id = fields.Many2one(
        comodel_name="ssi_hr.employee",
        string="Real Manager",
        tracking=True,
    )
    pic_manager_id = fields.Many2one(
        comodel_name="ssi_hr.employee",
        string="PIC Manager",
        tracking=True,
    )
    is_pic = fields.Boolean(
        string="PIC",
        default=False,
    )
    pic_start_date = fields.Date(
        string="Start Date",
    )
    pic_end_date = fields.Date(
        string="End Date",
    )
    note = fields.Text(
        string="Note",
    )
    color = fields.Integer(
        string="Color Index",
    )

    def name_get(self):
        if not self.env.context.get("hierarchical_naming", True):
            return [(record.id, record.name) for record in self]
        return super(Department, self).name_get()

    @api.model
    def name_create(self, name):
        return self.create({"name": name}).name_get()[0]

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = "{} / {}".format(
                    department.parent_id.complete_name,
                    department.name,
                )
            else:
                department.complete_name = department.name

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive departments."))
