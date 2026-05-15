from odoo import models, fields, api

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    puntaje_desempenio = fields.Integer(string='Puntaje de desempeño', related='employee_id.puntaje_desempenio', readonly=True)
    is_current_user = fields.Boolean(compute='_compute_is_current_user', store=False)

    @api.depends_context('uid')
    def _compute_is_current_user(self):
        for record in self:
            record.is_current_user = (record.user_id == self.env.user)
