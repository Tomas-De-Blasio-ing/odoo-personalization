from odoo import models, fields, api
from datetime import timedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    # --------------------------------------------------------------------------    
    # Campos del empleado que se agregan para puntaje_desempenio
    # --------------------------------------------------------------------------  

    puntaje_desempenio = fields.Integer(string = 'Puntaje de desempeño del empleado', compute = 'calculate_puntaje_desempenio', store=True)

    presencias_totales = fields.Integer(string = 'Presencias_totales', compute = 'sumar_dias', store=True)

    habiles_totales = fields.Integer(string = 'Días hábiles totales', compute = 'sumar_dias', store=True)

    antiguedad_fija  = fields.Integer(compute = 'calcular_antiguedad_fija', store=True)

    antiguedad_total  = fields.Integer(string = 'Antiguedad total', compute = 'calcular_antiguedad_total', store=True)


    @api.depends('slip_ids.dias_trabajados', 'slip_ids.dias_habiles')
    def sumar_dias(self):
        for record in self:
            record.presencias_totales = sum(record.slip_ids.mapped('dias_trabajados'))
            record.habiles_totales = sum(record.slip_ids.mapped('dias_habiles'))


    @api.depends('cantidad_titulos_uni','presencias_totales','habiles_totales','antiguedad_total')
    def calculate_puntaje_desempenio(self):
        for record in self:
            valor_ant = record.antiguedad_total
            if (record.habiles_totales != 0):
                porcentaje_prescencias = record.presencias_totales / record.habiles_totales
            else: 
                porcentaje_prescencias = 0
            cant_titulos =  record.cantidad_titulos_uni #(heredado de titulo.py)
            dic_titulos = {1: 10, 2: 15}
            if cant_titulos < 3:
                valor_tit = dic_titulos.get(cant_titulos,0)
            else: 
                valor_tit= 20
            if valor_ant < 20:
                valor_ant = valor_ant * 2
            else:
                valor_ant = 40
            valor_pres = 40 * porcentaje_prescencias
            record.puntaje_desempenio = valor_ant + valor_pres + valor_tit

    @api.depends('contract_ids.state')
    def calcular_antiguedad_fija(self):
        for record in self:
            suma_ant_fija = timedelta(0)
            contratos_cerrados = record.contract_ids.filtered(lambda x : x.state in ('cancel','close')) 
            for contratos in contratos_cerrados:
                if contratos.date_end and contratos.date_start:
                    suma_ant_fija += ((contratos.date_end)-(contratos.date_start))
            record.antiguedad_fija = (suma_ant_fija.days)


    @api.depends('contract_ids.state','antiguedad_fija','contract_ids.date_start')
    def calcular_antiguedad_total(self):
        for record in self:
            suma_ant = timedelta(0)
            contratos_actuales =record.contract_ids.filtered(lambda x : x.state in ('open'))
            for contratos in contratos_actuales:
                if contratos.date_start:
                    suma_ant += fields.Date.today() - contratos.date_start
            record.antiguedad_total = int((suma_ant.days + record.antiguedad_fija)/365)
