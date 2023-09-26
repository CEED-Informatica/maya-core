# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError

class Student(models.Model):
  """
  Define un estudiante
  """

  _name = 'maya_core.student'
  _description = 'Estudiante'
  _order = 'surname'

  moodle_id = fields.Char(string = 'moodle_id', size = 9, required = True)
  nia = fields.Char(string = 'NIA', size = 9)
  name = fields.Char(string = 'Nombre', required = True)
  surname = fields.Char(string = 'Apellidos', required = True)
  email = fields.Char(string = 'Email')

  student_info = fields.Char(string = 'Nombre completo', compute = '_compute_full_student_info')

  # puede estar matriculado en varios ciclos
  courses_ids = fields.Many2many('maya_core.course')
  # un estudiante podría solicitar convalidaciones de dos ciclos diferentes 
  # (aunque a día de hoy no está permitido)
  """ validations_ids = fields.One2many('maya_core.validation', 'student_id')"""
  """ subjects_ids = fields.Many2many('maya_core.subject',
    string = 'Módulos',
    relation = 'maya_core_subject_student_rel', 
    column1 = 'student_id', column2 = 'subject_id') """
  subjects_ids = fields.One2many('maya_core.subject_student_rel', 'student_id')
  
  def _compute_full_student_info(self):
    for record in self:
      record.student_info = record.surname + ', ' + record.name