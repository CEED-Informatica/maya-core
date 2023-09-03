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

  # Aulas virtuales asigndas a este módulo
  classrooms_ids = fields.One2many('maya_core.subject_classroom_rel', 'subject_id', string = 'Aulas virtuales')

  students_ids = fields.Many2many(
    'maya_core.student', 
    string = 'Estudiante',
    # ojo! la definición de la tabla lleva incluído el npmbre del módulo separado por _
    relation = 'maya_core_subject_student_rel', 
    column1 = 'subject_id', column2 = 'student_id')
  
  def get_classroom_by_course_id(self, course):
    """
    Devuelve el aula virtual asociada a este módulo para un ciclo determinado
    """
    self.ensure_one()
     
    return self.classrooms_ids.filtered(lambda t: t.course_id.id == course.id)['classroom_id']