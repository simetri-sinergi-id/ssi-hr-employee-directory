# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee Directory",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/ssi-hr-employee-directory",
    "category": "Human Resources/Employees",
    "summary": "Centralize Employee Information",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "data": [
        "menu.xml",
        "views/ssi_hr_department_type_view.xml",
        "views/ssi_hr_department_view.xml",
        "views/ssi_hr_employee_category_view.xml",
        "views/ssi_hr_job_grade_category_view.xml",
        "views/ssi_hr_job_grade_view.xml",
        "views/ssi_hr_job_family_view.xml",
        "views/ssi_hr_job_family_grade_view.xml",
        "views/ssi_hr_job_position_view.xml",
        "views/ssi_hr_employment_status_view.xml",
        "views/ssi_hr_employee_status_view.xml",
        "views/ssi_hr_employee.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/ssi_hr_employee_directory_demo.xml",
    ],
    "depends": [
        "contacts",
        "base_setup",
        "mail",
        "resource",
        "web",
    ],
}
