from odoo import models, fields, api

class MinisterioTitulo(models.Model):
    _name = 'ministerio.titulo'
    _description = 'Titulos de los docentes'
    _inherit = ['mail.thread','mail.activity.mixin'] #(mensajes y notas)(ver actividades)
    

    # --------------------------------------------------------------------------    
    # Campos de un título
    # --------------------------------------------------------------------------  

    name = fields.Char(string = 'Nombre del titulo', required=True)
    nivel = fields.Selection([
        ('secundario', 'Secundario'),
        ('terciario','Terciario'),
        ('universitario', 'Universitario')
    ], string='Nivel', default='terciario')
    
    #Se crea la columna fisica en la base de datos
    employee_id = fields.Many2one(
        'hr.employee', 
        string= 'Docente',
        # self.env.user es el usuario actual, .employee_id busca el id de la ficha del empleado
        default = lambda self: self.env.user.employee_id)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved','Aprobado')
    ], string = 'Estado', default='draft', tracking=True)
 
    # store = True, si no se agrega, se calcula el puntaje en el aire y no se guarda en la bd
    puntaje_boni= fields.Integer(string = 'Puntaje de bonificación', compute = '_compute_puntaje', store=True)

    es_grado_superior = fields.Boolean(string='Es Grado Superior')


    # --------------------------------------------------------------------------    
    # Funciónes de botones para el formulario
    # --------------------------------------------------------------------------    
    # Se crea la función que ejecutará el botón de estado de un título: "Aprobar Título"
    def action_aprobar(self):
        # Se itera sobre todos los titulos, por si se aprueban
        #  10 titulos a la vez
        for record in self:
            record.state = 'approved'

    def action_borrador(self):
        for record in self:
            record.state = 'draft'    
    


    # --------------------------------------------------------------------------    
    # Campos calculados @api.depends
    # --------------------------------------------------------------------------    
    @api.depends('nivel')
    def _compute_puntaje(self):
        """
        Calcula el puntaje automáticamente basado en el nivel del título.
        """
        for record in self:
            if record.nivel == 'secundario':
                record.puntaje_boni = 10
            elif record.nivel == 'terciario':
                record.puntaje_boni = 20
            elif record.nivel == 'universitario':
                record.puntaje_boni = 40
            else:
                record.puntaje_boni = 0