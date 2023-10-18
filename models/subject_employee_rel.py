# -*- coding: utf-8 -*-

from odoo import models, fields


class SubjectEmployeeRel(models.Model): 
  """
  Se crea como tabla de relación (pivote) entre Subject y Employee para dar soporte a un campo intermedio
  Sólo tiene sentido cuando el empleado sea un profesor
  """
  _name = 'maya_core.subject_employee_rel' 
  _description = 'Relación entre employee y subject' 

  subject_id = fields.Many2one('maya_core.subject', required = True)
  employee_id = fields.Many2one('maya_core.employee', required = True) 

  # ciclo en el que está matriculado
  course_id = fields.Many2one('maya_core.course', required = True)

  _sql_constraints = [ 
    ('unique_subject_employee_rel', 'unique(employee_id, subject_id, course_id)', 
       'Sólo puede haber una relación por empleado, ciclo y módulo.'),
  ]

