from odoo import api, models, fields

class Subject(models.Model):
    """
    Define un módulo (asignatura)
    """
      
    _name = 'maya_core.subject'
    _description = 'Módulo de un ciclo formativo'

    abbr = fields.Char(size = 4, required = True, translate = True, string = "Abreviatura")
    code = fields.Char(size = 6, required = True, string = "Código")
    name = fields.Char(required = True, translate = True, string = "Nombre")
    year = fields.Selection([('1', '1º'), ('2', '2º')], required = True, default = '1', string = 'Curso')

    courses_ids = fields.Many2many('maya_core.course', string = 'Ciclos', help = 'Ciclos en los que se imparte')
 