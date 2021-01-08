# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class JobPosition(models.Model):

    _name = "ssi_hr.job_position"
    _description = "Job Position"
    _inherit = ["mail.thread"]
    _rec_name = "complete_name"

    @api.depends("job_family_grade_id")
    def _compute_job_grade(self):
        for job in self:
            result = False
            if job.job_family_grade_id:
                result = job.job_family_grade_id.job_grade_ids.ids
            job.allowed_job_grade_ids = result

    name = fields.Char(
        string="Job Position",
        required=True,
        index=True,
        translate=True,
    )
    complete_name = fields.Char(
        string="Complete Name",
        compute="_compute_complete_name",
        store=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Job Description",
    )
    requirements = fields.Text(
        string="Requirements",
    )
    department_id = fields.Many2one(
        comodel_name="ssi_hr.department",
        string="Department",
        required=True,
        # domain="["|", ("company_id", "=", False),
        # ("company_id", "=", company_id)]",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    state = fields.Selection(
        [("recruit", "Recruitment in Progress"), ("open", "Not Recruiting")],
        string="Status",
        readonly=True,
        required=True,
        tracking=True,
        copy=False,
        default="recruit",
        help="Set whether the recruitment process is open or closed for this job position.",
    )
    no_of_recruitment = fields.Integer(
        string="Expected New Employees",
        copy=False,
        help="Number of new employees you expect to recruit.",
        default=1,
    )
    no_of_hired_employee = fields.Integer(
        string="Hired Employees",
        copy=False,
        help="Number of hired employees for this job position during recruitment phase.",
    )
    job_family_grade_id = fields.Many2one(
        string="Job Family Grade",
        comodel_name="ssi_hr.job_family_grade",
    )
    allowed_job_grade_ids = fields.Many2many(
        string="Job Grades",
        comodel_name="ssi_hr.job_grade",
        compute="_compute_job_grade",
        store=False,
    )
    job_grade_ids = fields.Many2many(
        string="Job Grades",
        comodel_name="ssi_hr.job_grade",
        relation="rel_job_2_grade",
        column1="job_position_id",
        column2="job_grade_id",
    )
    employee_ids = fields.One2many(
        comodel_name="ssi_hr.employee",
        inverse_name="job_position_id",
        string="Employees",
        readonly=True,
    )
    # expected_employees = fields.Integer(
    #     compute="_compute_employees",
    #     string="Total Forecasted Employees",
    #     store=True,
    #     help="Expected number of employees for this job position after new recruitment.",
    # )
    # no_of_employee = fields.Integer(
    #     compute="_compute_employees",
    #     string="Current Number of Employees",
    #     store=True,
    #     help="Number of employees currently occupying this job position.",
    # )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id, department_id)",
            "The name of the job position must be unique per department in company!",
        ),
    ]

    @api.depends("name", "department_id")
    def _compute_complete_name(self):
        for job in self:
            if job.department_id:
                job.complete_name = "{} {}".format(
                    job.name,
                    job.department_id.name,
                )
            else:
                job.complete_name = job.name

    # @api.depends("no_of_recruitment", "employee_ids.job_postion_id", "employee_ids.active")
    # def _compute_employees(self):
    #     employee_data = self.env["ssi_hr.employee"].read_group([("job_position_id", "in", self.ids)], ["job_position_id"], ["job_position_id"])
    #     result = dict((data["job_position_id"][0], data["job_position_id_count"]) for data in employee_data)
    #     for job_position in self:
    #         job_position.no_of_employee = result.get(job_position.id, 0)
    #         job_position.expected_employees = result.get(job_position.id, 0) + job_position.no_of_recruitment
    #
    # @api.model
    # def create(self, values):
    #     """ We don't want the current user to be follower of all created job """
    #     return super(JobPosition, self.with_context(mail_create_nosubscribe=True)).create(values)
    #
    # @api.returns("self", lambda value: value.id)
    # def copy(self, default=None):
    #     self.ensure_one()
    #     default = dict(default or {})
    #     if "name" not in default:
    #         default["name"] = _("%s (copy)") % (self.name)
    #     return super(JobPosition, self).copy(default=default)
    #
    # def set_recruit(self):
    #     for record in self:
    #         no_of_recruitment = 1 if record.no_of_recruitment == 0 else record.no_of_recruitment
    #         record.write({"state": "recruit", "no_of_recruitment": no_of_recruitment})
    #     return True
    #
    # def set_open(self):
    #     return self.write({
    #         "state": "open",
    #         "no_of_recruitment": 0,
    #         "no_of_hired_employee": 0
    #     })

    def onchange_job_family_grade_id(self, job_family_grade_id):
        value = self._get_value_before_onchange_job_family_grade_id()
        domain = self._get_domain_before_onchange_job_family_grade_id()

        if job_family_grade_id:
            obj_job_family_grade = self.env["ssi_hr.job_family_grade"]
            job_family_grade = obj_job_family_grade.browse([job_family_grade_id])[0]
            value = self._get_value_after_onchange_job_family_grade_id(job_family_grade)
            domain = self._get_domain_after_onchange_job_family_grade_id(
                job_family_grade
            )
        return {"value": value, "domain": domain}

    def _get_value_before_onchange_job_family_grade_id(self):
        return {
            "job_grade_ids": [],
        }

    def _get_domain_before_onchange_job_family_grade_id(self):
        return {}

    def _get_value_after_onchange_job_family_grade_id(self, job_family_grade):
        return {
            "job_grade_ids": [],
        }

    def _get_domain_after_onchange_job_family_grade_id(self, job_family_grade):
        return {}
