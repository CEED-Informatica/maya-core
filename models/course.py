from odoo import models, fields

class Course(models.Model):
    """
    Define un ciclo formativo
    """

    _name = 'maya_core.course'
    _description = 'Ciclo Formativo'

    abbr = fields.Char('Abreviatura', size = 5,required = True, translate=True)
    name = fields.Char('Ciclo', required = True, translate=True)