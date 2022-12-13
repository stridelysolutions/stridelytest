# -*- coding: utf-8 -*-

from odoo import models, api


class WhatsappDashboard(models.Model):
   _inherit = 'project.project'
   
   @api.model
   def get_tiles_data(self):
       print("====================")
       all_partner = self.env['res.partner'].search_read([])
       name_list = []
       for i in all_partner:
           name_list.append(i)
#        all_task = self.env['project.task'].search([])
#        analytic_project = self.env['account.analytic.line'].search([])
#        total_time = sum(analytic_project.mapped('unit_amount'))
#        employees = self.env['hr.employee'].search([])
#        task = self.env['project.task'].search_read([
#            ('sale_order_id', '!=', False)
#        ], ['sale_order_id'])
#        task_so_ids = [o['sale_order_id'][0] for o in task]
#        sale_orders = self.mapped('sale_line_id.order_id') | self.env['sale.order'].browse(task_so_ids)
       return {
           'all_partner':name_list,
           'total_projects': 2,
           'total_tasks': 3,
           'total_employees': 4,
       }

# class HrEmployee(models.Model):
#    _inherit = 'hr.employee'
   
#    @api.onchange('category_ids')
#    def test(self):
#        print("=============================")
#        childs = self.env['hr.leave.allocation']
#        search_allocations = self.env['hr.leave.allocation'].search([('category_id','in',self.category_ids._origin.ids)])
#        if search_allocations:
#             print("=================================",search_allocations.number_of_days)
#             employees = search_allocations.category_id.employee_ids
#             # allocation_create_vals = search_allocations._prepare_holiday_values(employees)
#             allocation_create_vals = [{
#             'name': search_allocations.name,
#             'holiday_type': 'category',
#             'holiday_status_id': search_allocations.holiday_status_id.id,
#             'notes': search_allocations.notes,
#             'number_of_days': search_allocations.number_of_days,
#             'parent_id': search_allocations.id,
#             'employee_id': employee.id,
#             'employee_ids': [(6, 0, [self._origin.id])],
#             'state': 'confirm',
#             'allocation_type': search_allocations.allocation_type,
#             'date_from': search_allocations.date_from,
#             'date_to': search_allocations.date_to,
#             'accrual_plan_id': search_allocations.accrual_plan_id.id,
#         } for employee in employees]
#             for i in allocation_create_vals:
#                 i['holiday_type'] = 'category'
#             print("===============================anbcd",allocation_create_vals)
#             childs.create(allocation_create_vals)
