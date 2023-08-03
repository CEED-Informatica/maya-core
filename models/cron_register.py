import logging
import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from ..support.constants import CRON_CONTEXTS
from dataclasses import dataclass

_logger = logging.getLogger(__name__)

@dataclass
class CronJobData:
  """
  Encapsula la información que se le puede pasar a las plantillas 
  """
  classroom_id: int = None
  course_id: int = None
  subject_id: int = None
  task_id: int = None


class CronRegister(models.Model):
  """
  Registra plantillas de todas las tareas cron posibles existentes
  Maya repasa todas ellas y genera tareas según el contexto 
  """
  _name = 'maya_core.cron_register'

  module = fields.Char(string = 'Módulo origen', help = 'Nombre del módulo que registra la tarea', compute= '_set_module', store = True)
  key = fields.Char(string = 'Clave', size = 5, required = True,  help = 'Clave para identificar la plantilla. Debe ser único')
  state = fields.Char(size = 4, default = 'code') 
  code = fields.Char(size = 5, required = True,  help = 'Método a ejecutar')
  context = fields.Char(string = 'Contexto', size = 4, required = True, help = 'Contexto en el que trabaja la tarea programada')
  name = fields.Char(string = 'Descripción', size = 80, required = True)
  model = fields.Char(size = 60, required = True, help = 'Nombre del modelo en el que estará el código a ejecutar')
  interval_number = fields.Integer(default = 1, help = 'Veces que se repite en el tipo de intervalo')
  interval_type = fields.Char(default = 'days', help = 'Unidad del intervalo')
  numbercall = fields.Integer(default = -1, help = 'Número de veces que será ejecutada la tarea')
  nextcall_day = fields.Char(required = True, help = 'Día de la primera ejecución. Soporta: \
                                                        día -> 2023/12/22 (ISO Format),\
                                                        campo de otro modelo -> school_year.date_init, \
                                                        día de la creación de la tarea -> today.\n\
                                                      Las dos últimas opcones adminte signo + y - para añadir o restar\
                                                      unidades de tipo interval_type: today + 2')
  nextcall_hour = fields.Char(required = True, help = 'Hora de la siguiente ejecución (ej: 18:20:50)')
  doall = fields.Boolean(default = True, help = 'Si el servidor cae, cuado se reinicie lanzará las tareas no ejecutadas')

  _sql_constraints = [ 
    ('unique_key', 'unique(key)', 'El código de la plantilla tiene que ser único.'),
  ]

  @api.constrains('interval_type')
  def _check_interval_type(self):
    for record in self:
      if record.interval_type not in ['minutes', 'hours', 'work_days', 'days', 'weeks', 'months']:
        raise ValidationError('Tipo de intervalo no soportado')
      
  @api.constrains('context')
  def _check_context(self):
    for record in self:
      if record.context not in CRON_CONTEXTS:
        raise ValidationError('Tipo de contexto no soportado')
      
  @api.constrains('nextcall_day')
  def _check_nextcall_day(self):
    for record in self:
      if record.nextcall_day.lower() == 'today':
        return
      
      if record.nextcall_day.lower().startswith('school_year.') == True:
        return
       
      try:
        datetime.date.fromisoformat(record.nextcall_day)
      except ValueError:
        raise ValidationError('Formato de día en nextcall no soportado')

  def _set_module(self):
    # TODO comprobar que el módulo sea un módulo de confianza
    for record in self:
      record.module = record._module

          