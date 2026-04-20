from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    es_grado_superior = fields.Boolean(string='Es Grado Superior?')


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
                record.es_grado_superior = False
            elif record.nivel == 'terciario':
                record.puntaje_boni = 20
                record.es_grado_superior = False
            elif record.nivel == 'universitario':
                record.puntaje_boni = 40
                record.es_grado_superior = True
            else:
                record.puntaje_boni = 0
                record.es_grado_superior = False

    # --------------------------------------------------------------------------    
    # Inteligencia de la interfaz @api.onchange
    # ---------------------------------------------------------------------    
    @api.onchange('nivel')
    def _onchange_aviso_analitico(self):
        """
        Lanza una advertencia visual si el usuario selecciona 'terciario'.
        """
        # Como es un onchange de un campo simple antes de guardar, 
        # a veces no necesitamos el "for record in self:", podemos usar self directo.
        for record in self:
            if self.nivel == 'terciario':
                return {
                    'warning': {
                        'title': "Aviso Importante",
                        'message': "Ha seleccionado nivel Terciario. Recuerde que es obligatorio adjuntar una copia escaneada del analítico en la pestaña de mensajes antes de solicitar la aprobación.",
                    }
                }

    # --------------------------------------------------------------------------    
    # Validación de integridad @api.constrains
    # ---------------------------------------------------------------------    
    @api.constrains('name','employee_id')
    def _chech_titulo_duplicado(self):
            '''
            Evita que un mismo docente se cargue dos veces exactamente con
            el mismo título
            ''' 
            for record in self:
                # Buscamos si existe otro registro con el mismo nombre y mismo docente
                # que NO sea este mismo registro (id != record.id)

                duplicados = self.search([
                    ('name', '=like',record.name), #=like ignora mayusculas/minúsculas
                    ('employee_id','=',record.employee_id.id),
                    ('id','!=',record.id)
                ])
                if duplicados:
                    raise ValidationError("Error: El docente ya tiene regitrado este título")

