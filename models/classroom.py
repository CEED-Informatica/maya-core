# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta, datetime

import os
import logging

_logger = logging.getLogger(__name__)

class Classroom(models.Model):
  """
  Define un aula virtual
  """

  _name = 'maya_core.classroom'
  _description = 'Aula virtual'
  _rec_name = 'code'

  moodle_id = fields.Integer('Identificador Moodle', required = True)
  code = fields.Char('Código', required = True, help = 'Código del aula, por ejemplo SEG9_CEE_46025799_2022_854101_0498')
  description = fields.Char('Descripción')

  # lo que se busca es una relación many2many con los módulos (subject) pero que incluya un campo más, el ciclo
  # ese campo lo quiero utilizar en las vistas además tratandolo (utilizando un compute para mostrar 
  # otra información). Para ello la solución más sencilla es dividir ese many2many es dos many2one
  subjects_ids = fields.One2many('maya_core.subject_classroom_rel', 'classroom_id')
  
  tasks_moodle_ids = fields.One2many('maya_core.task_moodle', 'classroom_id', string = 'Tareas que están conectadas con Maya')

  lang_id = fields.Many2one('res.lang', domain = [('active','=', True)], string = 'Idioma')

  _sql_constraints = [ 
    ('unique_moodle_id', 'unique(moodle_id)', 'El identificador de moodle tiene que ser único.'),
  ]

  def get_task_id_by_key(self, key):
    """ Devuelve la tarea encargada de las convalidaciones """  
    tasks = list(filter(lambda item: item['key'] == key, self.tasks_moodle_ids))
    if not tasks:
      _logger.error("No hay tarea de convalidaciones en el aula")
      return None

    return tasks[0].moodle_id