# -*- coding: utf-8 -*-

from odoo import models, fields

class Rol(models.Model):
    """
    Define los posibles roles del profesorado
    """
      
    _name = 'maya_core.rol'
    _description = 'Rol de profesorado'

    _rec_name = 'rol'
    _order = 'departament_id, course_id'

    rol = fields.Char('Cargo', size = 6, required = True)
    course_id = fields.Many2one('maya_core.course', string = 'Ciclo')
    departament_id = fields.Many2one('maya_core.departament', 'Departamento')
    description = fields.Char('Descripción', required = True)
    
