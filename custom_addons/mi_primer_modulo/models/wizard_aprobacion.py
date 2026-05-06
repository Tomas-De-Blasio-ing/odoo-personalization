from odoo import models, fields

class WizardAprobacionTitulo(models.TransientModel):
    _name = 'wizard.aprobacion.titulo'
    _description = 'Wizard para aprobación masiva'

    # --------------------------------------------------------
    # Campos del wizard
    # ---------------------------------------------------------
    comentario = fields.Text(string = 'Comentarios de aprobación')



    # -------------------------------------------------------------
    # Acción de confirmación
    # --------------------------------------------------------

    def action_aprobacion_masiva(self):
        # 1. Se utiliza la variable 'context' para pasar datos entre pantallas.
        #    Cuando se abre un wizard de una lista, Odoo guarda los IDs de los
        #    registros que fueron selecicondos en la varibale 'active_ids'.
        titulos_selec = self.env.context.get('active_ids',[])

        # 2. Buscamos esos títulos en la base de datos
        titulos = self.env['ministerio.titulo'].browse(titulos_selec)

        # 3. Iteramos y aprobamos
        for titulo in titulos:
            titulo.state = 'approved'
            if self.comentario:
                titulo.message_post(body=f"Aprobado masivamente. Nota {self.comentario}") 