from odoo import models, fields, api

class MinisterioTitulo(models.Model):
    _name = 'ministerio.titulo'
    _description = 'Titulos de los docentes'
    _inherit = ['mail.thread','mail.activity.mixin'] #(menajes y notas)(ver actividades)

    name = fields.Char(string = 'Nombre del titulo', required=True)
    nivel = fields.Selection([
        ('terciario','Terciario'),
        ('universitario', 'Universitario')
    ], string='Nivel', default='terciario')
    
    #Se crea la columna fisica en la base de datos
    employee_id = fields.Many2one('hr.employee', string= 'Docente')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved','Aprobado')
    ], string = 'Estado', default='draft', tracking=True)





    # Se crea la función que ejecutará el botón de estado de un título: "Aprobar Título"
    def action_aprobar(self):
        # Se itera sobre todos los titulos, por si se aprueban
        #  10 titulos a la vez
        for record in self:
            # Cambiamos el valor del campo a 'approved'
            record.state = 'approved'

    def action_borrador(self):
        # Se itera sobre todos los titulos, por si se aprueban
        #  10 titulos a la vez
        for record in self:
            # Cambiamos el valor del campo a 'approved'
            record.state = 'draft'    
    