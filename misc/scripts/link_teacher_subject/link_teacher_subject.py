#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import csv
import sys, argparse

def print_dictionary(dictionary):
  """
  Muestra por pantalla un diccionario de una manera más ordenada
  """
  for key, value in dictionary.items():  
    print(' * {} ({})'.format(key, value))

def print_list(list):
  """
  Muestra por pantalla una lista de una manera más ordenada
  """
  for value in list:  
    print(' * {}'.format(value))

print('\033[1mMaya | link-subject-techer. v1.0\033[0m')

parser = argparse.ArgumentParser(
  description = 'Enlaza profesores (employee) y con módulos (subject) desde un csv')

# argumentos
parser.add_argument('csv_filename', help = 'Fichero csv con los datos: login,course,subject,course,subject,...') 
parser.add_argument('-u', '--url', default = 'http://localhost', help = 'URL del servidor Odoo. Por defecto: http://localhost')
parser.add_argument('-p', '--port', default = '8069', help = 'Puerto del servidor Odoo. Por defecto: 8069')
parser.add_argument('-db', '--database', required = True, help = 'Base de datos. Requerido')
parser.add_argument('-sr', '--user', default = 'admin', help = 'Usuario administrador Odoo. Por defecto: admin')
parser.add_argument('-ps', '--password', default = 'admin', help = 'Contraseña usuario administrador Odoo. Por defecto: admin')

args = parser.parse_args()

url = args.url + ':' + args.port
db = args.database
username = args.user
password = args.password

teacher_subjects = {}

# end point xmlrpc/2/common permite llamadas sin autenticar
print('\033[0;32m[INFO]\033[0m Conectando con',url, ' -> ', db)
try:
  common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
  print('\033[0;32m[INFO]\033[0m Odoo server', common.version()['server_version'])
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print('\033[0;31m[ERROR]\033[0m Compruebe que el servidor de Odoo esté arrancado')
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

# autenticación
uid = common.authenticate(db, username, password, {})

try:
  with open(args.csv_filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    for row in csv_reader:
      if line_count > 0:
        # almaceno los módulos
        subjects_row = row[1:]
        if len(subjects_row) > 0 and len(subjects_row) % 2 == 0: # tienen que ser parejas
          teacher_subjects[row[0]] = [(subjects_row[i], 
                                       subjects_row[i + 1][:subjects_row[i + 1].find('-')].strip(), 
                                       subjects_row[i + 1][(subjects_row[i + 1].find('-')+1):].strip()) 
                                       for i in range(0, len(subjects_row), 2)]
        else:
          raise Exception(f'El usuario {row[0]} no tiene módulos asignados o el número de ciclos no coincide con el de módulos')

      line_count += 1
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()     

print('\033[0;32m[INFO]\033[0m Usuarios en csv:', len(teacher_subjects))    

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

try:
  # ciclos
  course_output = models.execute_kw(db, uid, password, 'maya_core.course', 'search_read', [[]], { 'fields':  ['abbr', 'id'] } )
  courses_ec = {}
  for course in course_output:
    courses_ec[course['abbr']] = course['id']

  print(f'\033[0;32m[INFO]\033[0m Ciclos:')
  print_dictionary(courses_ec)

  # módulos
  subject_output = models.execute_kw(db, uid, password, 'maya_core.subject', 'search_read', [[]], { 'fields':  ['abbr', 'code', 'id', 'courses_ids']})
  subjects_ec = {}
  for subj in subject_output:
    subjects_ec[subj['code']] = [subj['id'], subj['courses_ids'] ]

  print(f'\033[0;32m[INFO]\033[0m Módulos:')
  print_dictionary(subjects_ec)

except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

line_count_OK = 0
line_count_ERROR = 0

for teacher in teacher_subjects:  
  print("\033[0;32m[INFO]\033[0m Procesando", teacher)
  try:
   
    # hay que buscar si el empleado existe.
    # obtengo el id del usuario
    id = models.execute_kw(db, uid, password, 'res.users', 'search_read', 
                                            [[['login','=', teacher]]], { 'fields': ['id', 'maya_employee_id']})
    
    if len(id) == 0:
      raise Exception(f'No existe el usuario {teacher} en Odoo.')
    
    if id[0]['maya_employee_id'] == False:
      raise Exception(f'No existe un empleado asociado al usuario {teacher}.')
    
    # se comprueba que la relación módulo/ciclo exista
    for subj in teacher_subjects[teacher]:
      if not any(course_id == courses_ec[subj[0]] for course_id in subjects_ec[subj[1]][1]):
         raise Exception(f'El módulo {subj[2]} no se cursa en {subj[0]}. Profesor {teacher}')

    # se eliminan, si las hay, las relaciones previas con otros módulos
    teacher_of_subjects = models.execute_kw(db, uid, password, 
                                            'maya_core.subject_employee_rel', 
                                            'search_read', 
                                            [[['employee_id','=', id[0]['maya_employee_id'][0]]]], { 'fields': ['id']})

    if len(teacher_of_subjects):
      for ids in teacher_of_subjects:
        models.execute_kw(db, uid, password, 'maya_core.subject_employee_rel', 'unlink', [[ids['id']]])

    # enlazo los módulos que imparte
    for subj in teacher_subjects[teacher]:
      models.execute_kw(db, uid, password, 'maya_core.subject_employee_rel','create', [{
        'course_id': courses_ec[subj[0]],
        'subject_id': subjects_ec[subj[1]][0],
        'employee_id': id[0]['maya_employee_id'][0]
      }])
      print("\033[0;32m[INFO]\033[0m\tAsociando ", teacher, "->", subj[2],"/", subj[0])

  except (xmlrpc.client.Fault) as e:
    print('   \033[0;31m[ERROR]\033[0m ' + e.faultString)
    line_count_ERROR += 1
  except KeyError:
    print('   \033[0;31m[ERROR]\033[0m Clave no encontrada. Posiblemente el departamento no existe')
    line_count_ERROR += 1
  except Exception as e:
    print('   \033[0;31m[ERROR]\033[0m ' + str(e))
    line_count_ERROR += 1

print(f'\033[0;32m[INFO]\033[0m Procesados {line_count_OK} usuarios / Errores: {line_count_ERROR}.')


