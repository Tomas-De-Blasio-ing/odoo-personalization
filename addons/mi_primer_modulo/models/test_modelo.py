from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_legajo_min = fields.Char(string="Legajo Ministerio", required=True, default = '0000')

   
    # OCULTAR FILTROS DE BÚSQUEDA
    # @api.model significa que esta funcion afecta a TODA la tabla
    @api.model
    def fields_get(self, allfields=None, attributes = None):
        # Se llama a super para trare la lista original
        res = super(HrEmployee, self).fields_get(allfields, attributes)

        campos_a_ocultar = [
            'create_uid', 'private_street',
            'departament_color', 'private_email',
            'km_home_work', 'private_state_id',
            'spouse_birthdate', 'visa_expire',
            'image_1920', 'image_1024', 'image_128',
            'image_256', 'image_512'
        ]
        # Buscamos el campo técnico
        
        for campo in campos_a_ocultar:
            if campo in res:
                # le apagamos el atributo que permite aparecer en los filtros
                res[campo]['searchable'] = False
    
        # Devolvemos la lista modeificada a la interefaz visual
        return res