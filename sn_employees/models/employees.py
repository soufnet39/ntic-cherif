# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class EmployeeCategory(models.Model):

    _name = "sn_employees.employee.category"
    _description = "Employee Category"

    name = fields.Char(string="Employee Tag", required=True)
    color = fields.Integer(string='Color Index')
    employee_ids = fields.Many2many('sn_employees.employee', 'employee_category_rel', 'category_id', 'emp_id', string='Employees')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Ce nom exist deja !"),
    ]


class Employee(models.Model):
    _name = "sn_employees.employee"
    _description = "Employee"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin']

    _mail_post_access = 'read'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    # resource and user
    # required on the resource, make sure required="True" set in the view
    name = fields.Char(related='resource_id.name', store=True, readonly=False)
    user_id = fields.Many2one('res.users', 'User', related='resource_id.user_id', store=True, readonly=False)
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True, readonly=False)
    # private partner
    address_home_id = fields.Many2one(
        'sn_sales.partner', 'Private Address', help='Enter here the private address of the employee, not the one linked to your company.',
        groups="sn_employees.group_sn_employees_user")
    is_address_home_a_company = fields.Boolean(
        'The employee adress has a company linked',
        compute='_compute_is_address_home_a_company',
    )
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="sn_employees.group_sn_employees_user")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="sn_employees.group_sn_employees_user", default="male")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="sn_employees.group_sn_employees_user", default='single')

    children = fields.Integer(string='Number of Children', groups="sn_employees.group_sn_employees_user")
    place_of_birth = fields.Char('Place of Birth', groups="sn_employees.group_sn_employees_user")
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", groups="sn_employees.group_sn_employees_user")
    birthday = fields.Date('Date of Birth', groups="sn_employees.group_sn_employees_user")
    identification_id = fields.Char(string='Identification No', groups="sn_employees.group_sn_employees_user")
    passport_id = fields.Char('Passport No', groups="sn_employees.group_sn_employees_user")
    bank_account_id = fields.Many2one(
        'sn_sales.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id)]",
        groups="sn_employees.group_sn_employees_user",
        help='Employee bank salary account')
    permit_no = fields.Char('Work Permit No', groups="sn_employees.group_sn_employees_user")
    additional_note = fields.Text(string='Additional Note', groups="sn_employees.group_sn_employees_user")
    certificate = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('other', 'Other'),
    ], 'Certificate Level', default='master', groups="sn_employees.group_sn_employees_user")
    study_field = fields.Char("Field of Study", placeholder='Computer Science', groups="sn_employees.group_sn_employees_user")
    study_school = fields.Char("School", groups="sn_employees.group_sn_employees_user")
    emergency_contact = fields.Char("Emergency Contact", groups="sn_employees.group_sn_employees_user")
    emergency_phone = fields.Char("Emergency Phone", groups="sn_employees.group_sn_employees_user")
    km_home_work = fields.Integer(string="Km home-work", groups="sn_employees.group_sn_employees_user")

    job_title = fields.Char("Job Title")

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Photo", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized photo", attachment=True,
        help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    # work
    address_id = fields.Many2one(
        'sn_sales.partner', 'Work Address')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    work_location = fields.Char('Work Location')
    # employee in company
    department_id = fields.Many2one('sn_employees.department', 'Department')
    parent_id = fields.Many2one('sn_employees.employee', 'Manager')
    child_ids = fields.One2many('sn_employees.employee', 'parent_id', string='Subordinates')
    coach_id = fields.Many2one('sn_employees.employee', 'Coach')
    category_ids = fields.Many2many(
        'sn_employees.employee.category', 'employee_category_rel',
        'emp_id', 'category_id',
        string='Tags')
    # misc
    notes = fields.Text('Notes')
    color = fields.Integer('Color Index', default=0)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('Vous ne pouvez pas créer une hiérarchie récursive.'))


    @api.onchange('address_id')
    def _onchange_address(self):
        self.work_phone = self.address_id.phone
        self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('department_id')
    def _onchange_department(self):
        self.parent_id = self.department_id.manager_id

    @api.onchange('user_id')
    def _onchange_user(self):
        if self.user_id:
            self.update(self._sync_user(self.user_id))

    @api.onchange('resource_calendar_id')
    def _onchange_timezone(self):
        if self.resource_calendar_id and not self.tz:
            self.tz = self.resource_calendar_id.tz

    def _sync_user(self, user):
        vals = dict(
            name=user.name,
            image=user.image,
            work_email=user.email,
        )
        if user.tz:
            vals['tz'] = user.tz
        return vals

    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        employee = super(Employee, self).create(vals)
        if employee.department_id:
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', employee.department_id.id)
            ])._subscribe_users()
        return employee

    def write(self, vals):
        if 'address_home_id' in vals:
            account_id = vals.get('bank_account_id') or self.bank_account_id.id
            if account_id:
                self.env['sn_sales.partner.bank'].browse(account_id).partner_id = vals['address_home_id']
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        res = super(Employee, self).write(vals)
        if vals.get('department_id') or vals.get('user_id'):
            department_id = vals['department_id'] if vals.get('department_id') else self[:1].department_id.id
            # When added to a department or changing user, subscribe to the channels auto-subscribed by department
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', department_id)
            ])._subscribe_users()
        return res

    def unlink(self):
        resources = self.mapped('resource_id')
        super(Employee, self).unlink()
        return resources.unlink()

    @api.depends('address_home_id.parent_id')
    def _compute_is_address_home_a_company(self):
        """Checks that choosen address (sn_sales.partner) is not linked to a company.
        """
        for employee in self:
            try:
                employee.is_address_home_a_company = employee.address_home_id.parent_id.id is not False
            except AccessError:
                employee.is_address_home_a_company = False

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Employees'),
            'template': '/sn_employees/static/xls/hr_employee.xls'
        }]


class Department(models.Model):
    _name = "sn_employees.department"
    _description = "HR Department"
    _inherit = ['mail.thread']
    _order = "name"
    _rec_name = 'complete_name'

    name = fields.Char('Department Name', required=True)
    complete_name = fields.Char('Nom Complèt', compute='_compute_complete_name', store=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id)
    parent_id = fields.Many2one('sn_employees.department', string='Parent Department', index=True)
    child_ids = fields.One2many('sn_employees.department', 'parent_id', string='Child Departments')
    manager_id = fields.Many2one('sn_employees.employee', string='Manager', track_visibility='onchange')
    member_ids = fields.One2many('sn_employees.employee', 'department_id', string='Members', readonly=True)
    note = fields.Text('Note')
    color = fields.Integer('Color Index')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Vous ne pouvez pas créer de relation récursive.'))

    @api.model
    def create(self, vals):
        # TDE note: auto-subscription of manager done by hand, because currently
        # the tracking allows to track+subscribe fields linked to a res.user record
        # An update of the limited behavior should come, but not currently done.
        department = super(Department, self.with_context(mail_create_nosubscribe=True)).create(vals)
        manager = self.env['sn_employees.employee'].browse(vals.get("manager_id"))
        if manager.user_id:
            department.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
        return department

    def write(self, vals):
        """ If updating manager of a department, we need to update all the employees
            of department hierarchy, and subscribe the new manager.
        """
        # TDE note: auto-subscription of manager done by hand, because currently
        # the tracking allows to track+subscribe fields linked to a res.user record
        # An update of the limited behavior should come, but not currently done.
        if 'manager_id' in vals:
            manager_id = vals.get("manager_id")
            if manager_id:
                manager = self.env['sn_employees.employee'].browse(manager_id)
                # subscribe the manager user
                if manager.user_id:
                    self.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
            # set the employees's parent to the new manager
            self._update_employee_manager(manager_id)
        return super(Department, self).write(vals)

    def _update_employee_manager(self, manager_id):
        employees = self.env['sn_employees.employee']
        for department in self:
            employees = employees | self.env['sn_employees.employee'].search([
                ('id', '!=', manager_id),
                ('department_id', '=', department.id),
                ('parent_id', '=', department.manager_id.id)
            ])
        employees.write({'parent_id': manager_id})
