# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
from ast import literal_eval
from datetime import timedelta
from random import choice
from string import digits

from pytz import UTC, timezone, utc

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.modules.module import get_module_resource
from odoo.tools import format_time


class HrEmployee(models.Model):
    _name = "ssi_hr.employee"
    _description = "Employee"
    _inherit = ["mail.thread"]
    _order = "name,id"

    name = fields.Char(
        string="Employee Name",
        required=True,
    )
    # employee base data
    active = fields.Boolean(string="Active", default=True)

    color = fields.Integer(string="Color Index", default=0)
    job_position_id = fields.Many2one(
        comodel_name="ssi_hr.job_position",
        string="Job Position",
    )
    employment_status_id = fields.Many2one(
        comodel_name="ssi_hr.employment_status", string="Employment Status"
    )
    employee_status_id = fields.Many2one(
        comodel_name="ssi_hr.employee_status", string="Employee Status"
    )
    # depertment depend on job position
    department_id = fields.Many2one(
        comodel_name="ssi_hr.department",
        string="Department",
    )
    # grade depend on job position
    job_grade_id = fields.Many2one(
        comodel_name="ssi_hr.job_grade",
        string="Job Grade",
    )
    job_title = fields.Char(
        string="Job Title",
        compute="_compute_job_title",
        store=True,
        readonly=False,
    )
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    address_id = fields.Many2one(
        comodel_name="res.partner",
        string="Work Address",
        compute="_compute_address_id",
        store=True,
        readonly=False,
    )
    work_phone = fields.Char(
        string="Work Phone",
        compute="_compute_phones",
        store=True,
        readonly=False,
    )
    mobile_phone = fields.Char(string="Work Mobile")
    work_email = fields.Char(string="Work Email")
    work_location = fields.Char(string="Work Location")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User ID",
    )
    resource_id = fields.Many2one(comodel_name="resource.resource", string="Resource")
    resource_calendar_id = fields.Many2one(
        comodel_name="resource.calendar",
        string="Resource Calendar",
    )
    parent_id = fields.Many2one(
        comodel_name="ssi_hr.employee",
        string="Manager",
        compute="_compute_parent_id",
        store=True,
        readonly=False,
    )
    coach_id = fields.Many2one(
        comodel_name="ssi_hr.employee",
        string="Coach",
        compute="_compute_coach",
        store=True,
        readonly=False,
    )
    tz = fields.Selection(
        string="Timezone",
        related="resource_id.tz",
        readonly=False,
        help="This field is used in order to define in which timezone the resources will work.",
    )
    hr_presence_state = fields.Selection(
        [("present", "Present"), ("absent", "Absent"), ("to_define", "To Define")],
        compute="_compute_presence_state",
        default="to_define",
    )
    last_activity = fields.Date(
        string="Last Activity",
        compute="_compute_last_activity",
    )
    last_activity_time = fields.Char(
        string="Last Activity Time",
        compute="_compute_last_activity",
    )
    hr_icon_display = fields.Selection(
        [
            ("presence_present", "Present"),
            ("presence_absent_active", "Present but not active"),
            ("presence_absent", "Absent"),
            ("presence_to_define", "To define"),
            ("presence_undetermined", "Undetermined"),
        ],
        compute="_compute_presence_icon",
    )
    # private partner
    address_home_id = fields.Many2one(
        comodel_name="res.partner",
        string="Address",
        help="Enter here the private address of the employee, not the one linked to your company.",
        # groups="hr.group_hr_user",
        tracking=True,
        # domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    is_address_home_a_company = fields.Boolean(
        string="The employee address has a company linked",
        compute="_compute_is_address_home_a_company",
    )
    private_email = fields.Char(
        related="address_home_id.email",
        string="Private Email",
        # groups="hr.group_hr_user",
    )
    phone = fields.Char(
        related="address_home_id.phone",
        related_sudo=False,
        readonly=False,
        string="Private Phone",
        # groups="hr.group_hr_user",
    )
    # employee in company
    child_ids = fields.One2many(
        comodel_name="ssi_hr.employee",
        inverse_name="parent_id",
        string="Direct subordinates",
    )
    category_ids = fields.Many2many(
        comodel_name="ssi_hr.employee.category",
        relation="ssi_employee_category_rel",
        column1="emp_id",
        column2="category_id",
        # groups="hr.group_hr_manager",
        string="Tags",
    )
    # misc
    identification_id = fields.Char(
        string="Identification No",
        # groups="hr.group_hr_user",
        tracking=True,
    )
    notes = fields.Text(
        string="Notes",
        # groups="hr.group_hr_user",
        # color = fields.Integer('Color Index', default=0, groups="hr.group_hr_user")
    )
    barcode = fields.Char(
        string="Badge ID",
        help="ID used for employee identification.",
        # groups="hr.group_hr_user",
        copy=False,
    )
    # pin = fields.Char(
    #     string="PIN",
    #     groups="hr.group_hr_user",
    #     copy=False,
    #     help="PIN used to Check In/Out in Kiosk Mode (if enabled in Configuration).",
    # )

    # Departure Information (resign)
    departure_description = fields.Text(
        string="Additional Information",
        # groups="hr.group_hr_user",
        copy=False,
        tracking=True,
    )
    departure_date = fields.Date(
        string="Departure Date",
        # groups="hr.group_hr_user",
        copy=False,
        tracking=True,
    )
    # message_main_attachment_id = fields.Many2one(groups="hr.group_hr_user")

    # Career Information
    first_join_date = fields.Date(
        string="First Join Date",
        copy=False,
        tracking=True,
        help="First time join date in company",
    )
    employed_date = fields.Date(
        string="Employed Date",
        copy=False,
        tracking=True,
        help="First time employed date in company",
    )
    permanent_date = fields.Date(
        string="Permanent Date",
        copy=False,
        tracking=True,
        help="Date become permanent employee in company",
    )
    start_contract_date = fields.Date(
        string="Start Contract Date",
        copy=False,
        tracking=True,
        help="Start contract date for non permanent employee",
    )
    end_contract_date = fields.Date(
        string="End Contract Date",
        copy=False,
        tracking=True,
        help="End contract date for non permanent employee",
    )
    evaluation_date = fields.Date(
        string="Evaluation Date",
        copy=False,
        tracking=True,
        help="Evaluation date for non employee .. opsional",
    )

    _sql_constraints = [
        (
            "barcode_uniq",
            "unique (barcode)",
            "The Badge ID must be unique, this one is already assigned to another employee.",
        ),
        (
            "user_uniq",
            "unique (user_id, company_id)",
            "A user cannot be linked to multiple employees in the same company.",
        ),
    ]

    @api.depends("user_id.im_status")
    def _compute_presence_state(self):
        """
        This method is overritten in several other modules which add additional
        presence criterions. e.g. hr_attendance, hr_holidays
        """
        # Check on login
        # check_login = literal_eval(self.env['ir.config_parameter'].sudo().get_param('hr.hr_presence_control_login', 'False'))
        check_login = False
        employee_to_check_working = self.filtered(lambda e: e.user_id.im_status)
        working_now_list = employee_to_check_working._get_employee_working_now()
        for employee in self:
            state = "to_define"
            if check_login:
                if employee.user_id.im_status == "online" or employee.last_activity:
                    state = "present"
                elif (
                    employee.user_id.im_status == "offline"
                    and employee.id not in working_now_list
                ):
                    state = "absent"
            employee.hr_presence_state = state

    @api.depends("user_id")
    def _compute_last_activity(self):
        presences = self.env["bus.presence"].search_read(
            [("user_id", "in", self.mapped("user_id").ids)],
            ["user_id", "last_presence"],
        )
        # transform the result to a dict with this format {user.id: last_presence}
        presences = {p["user_id"][0]: p["last_presence"] for p in presences}

        for employee in self:
            tz = employee.tz
            last_presence = presences.get(employee.user_id.id, False)
            if last_presence:
                last_activity_datetime = (
                    last_presence.replace(tzinfo=UTC)
                    .astimezone(timezone(tz))
                    .replace(tzinfo=None)
                )
                employee.last_activity = last_activity_datetime.date()
                if employee.last_activity == fields.Date.today():
                    employee.last_activity_time = format_time(
                        self.env, last_activity_datetime, time_format="short"
                    )
                else:
                    employee.last_activity_time = False
            else:
                employee.last_activity = False
                employee.last_activity_time = False

    @api.depends("parent_id")
    def _compute_coach(self):
        for employee in self:
            manager = employee.parent_id
            previous_manager = employee._origin.parent_id
            if manager and (
                employee.coach_id == previous_manager or not employee.coach_id
            ):
                employee.coach_id = manager
            elif not employee.coach_id:
                employee.coach_id = False

    @api.depends("job_position_id")
    def _compute_job_title(self):
        for employee in self.filtered("job_position_id"):
            employee.job_title = employee.job_position_id.name

    @api.depends("address_id")
    def _compute_phones(self):
        for employee in self:
            if employee.address_id and employee.address_id.phone:
                employee.work_phone = employee.address_id.phone
            else:
                employee.work_phone = False

    @api.depends("company_id")
    def _compute_address_id(self):
        for employee in self:
            address = employee.company_id.partner_id.address_get(["default"])
            employee.address_id = address["default"] if address else False

    @api.depends("department_id")
    def _compute_parent_id(self):
        for employee in self.filtered("department_id.manager_id"):
            employee.parent_id = employee.department_id.manager_id

    @api.depends("resource_calendar_id", "hr_presence_state")
    def _compute_presence_icon(self):
        """
        This method compute the state defining the display icon in the kanban view.
        It can be overriden to add other possibilities, like time off or attendances recordings.
        """
        working_now_list = self._get_employee_working_now()
        for employee in self:
            if employee.hr_presence_state == "present":
                if employee.id in working_now_list:
                    icon = "presence_present"
                else:
                    icon = "presence_absent_active"
            elif employee.hr_presence_state == "absent":
                # employee is not in the working_now_list and he has a user_id
                icon = "presence_absent"
            else:
                # without attendance, default employee state is 'to_define' without confirmed presence/absence
                # we need to check why they are not there
                if employee.user_id:
                    # Display an orange icon on internal users.
                    icon = "presence_to_define"
                else:
                    # We don't want non-user employee to have icon.
                    icon = "presence_undetermined"
            employee.hr_icon_display = icon

    @api.model
    def _get_employee_working_now(self):
        working_now = []
        # We loop over all the employee tz and the resource calendar_id to detect working hours in batch.
        all_employee_tz = self.mapped("tz")
        for tz in all_employee_tz:
            employee_ids = self.filtered(lambda e: e.tz == tz)
            resource_calendar_ids = employee_ids.mapped("resource_calendar_id")
            for calendar_id in resource_calendar_ids:
                res_employee_ids = employee_ids.filtered(
                    lambda e: e.resource_calendar_id.id == calendar_id.id
                )
                start_dt = fields.Datetime.now()
                stop_dt = start_dt + timedelta(hours=1)
                from_datetime = utc.localize(start_dt).astimezone(timezone(tz or "UTC"))
                to_datetime = utc.localize(stop_dt).astimezone(timezone(tz or "UTC"))
                # Getting work interval of the first is working. Functions called on resource_calendar_id
                # are waiting for singleton
                work_interval = res_employee_ids[
                    0
                ].resource_calendar_id._work_intervals(from_datetime, to_datetime)
                # Employee that is not supposed to work have empty items.
                if len(work_interval._items) > 0:
                    # The employees should be working now according to their work schedule
                    working_now += res_employee_ids.ids
        return working_now

    def generate_random_barcode(self):
        for employee in self:
            employee.barcode = "041" + "".join(choice(digits) for i in range(9))

    @api.depends("address_home_id.parent_id")
    def _compute_is_address_home_a_company(self):
        """Checks that chosen address (res.partner) is not linked to a company."""
        for employee in self:
            try:
                employee.is_address_home_a_company = (
                    employee.address_home_id.parent_id.id is not False
                )
            except AccessError:
                employee.is_address_home_a_company = False
