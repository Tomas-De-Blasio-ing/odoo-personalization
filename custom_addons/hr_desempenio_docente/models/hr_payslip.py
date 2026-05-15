from odoo import models, fields, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    # --------------------------------------------------------------------------    
    # Campos del payslip que se agregan para puntaje_desempenio
    # --------------------------------------------------------------------------  

    dias_trabajados = fields.Integer(string = 'Dias trabajados')

    dias_habiles = fields.Integer(string = 'Dias hábiles')

    