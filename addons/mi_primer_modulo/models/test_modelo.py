from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    # --------------------------------------------------------------------------    
    # Campos de un título
    # --------------------------------------------------------------------------  

    legajo_ministerio = fields.Char(string="Legajo Ministerio", required=True, default = '0000')
    cantidad_titulos = fields.Integer(string="Cantidad de Títulos", compute="_compute_cantidad_titulos")



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



    # --------------------------------------------------------------------------    
    # Contar cantidad de títulos con método search
    # ---------------------------------------------------------------------    
    def _compute_cantidad_titulos(self):
        for record in self:
            # 2. Viajamos a la tabla de títulos usando self.env
            # 3. Usamos .search() pasándole un "Dominio" (Condición de búsqueda)
            titulos_encontrados = self.env['ministerio.titulo'].search([
                ('empleado_id', '=', record.id), # Que el título sea de este empleado
                ('nivel', '=', 'universitario')  # Que sea universitario
            ])
            
            # 4. Contamos cuántos encontró (len es una función de Python para contar)
            record.cantidad_titulos = len(titulos_encontrados)
