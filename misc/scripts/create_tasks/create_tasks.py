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


print('\033[1mMaya | create-tasks. v1.1\033[0m')

parser = argparse.ArgumentParser(
  description = 'Crea en Maya, a partir de un fichero .csv, las tareas Moodle que se vinculan')

# argumentos
parser.add_argument('csv_filename', help = 'Fichero csv con los datos: id,key,description,course_abbr,classroom_code ') 
parser.add_argument('-u', '--url', default = 'http://localhost', help = 'URL del servidor Odoo. Por defecto: http://localhost')
parser.add_argument('-p', '--port', default = '8069', help = 'Puerto del servidor Odoo. Por defecto: 8069')
parser.add_argument('-db', '--database', required = True, help = 'Base de datos. Requerido')
parser.add_argument('-sr', '--user', default = 'admin', help = 'Usuario administrador Odoo. Por defecto: admin')
parser.add_argument('-ps', '--password', default = 'admin', help = 'Contraseña usuario administrador Odoo. Por defecto: admin')

args = parser.parse_args()
url = "http://localhost:8069"
db = "TEST_CEED_Aules_2022"
username = 'admin'
password = 'admin'

# tipo de keys soportadas
tasks_keys = ['validation', 'validation_claim', 'competence', 'competence_claim', 'pfc_1', 'pfc_2', 'cancel', 'renounce']

url = args.url + ':' + args.port
db = args.database
username = args.user
password = args.password

tasks = []

try:
  # end point xmlrpc/2/common permite llamadas sin autenticar
  print('\033[0;32m[INFO]\033[0m Conectando con',url)
  common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
  print('\033[0;32m[INFO]\033[0m Odoo server', common.version()['server_version'])
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print('\033[0;31m[ERROR]\033[0m Compruebe que el servidor de Odoo esté arrancado')
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

# autenticación
uid = common.authenticate(db, username, password, {})

with open(args.csv_filename) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter = ',')
  line_count = 0
  for row in csv_reader:
    if line_count > 0:
      tasks.append({
          'moodle_id': row[0],
          'key': row[1],
          'description': row[2],
          'course_abbr': row[3],
          'classroom_code': row[4]
      })
    line_count += 1

print('\033[0;32m[INFO]\033[0m Tareas en csv:', len(tasks))

try:
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

  # obtengo todos los ciclos
  courses_output = models.execute_kw(db, uid, password, 'maya_core.course', 'search_read', [[]], { 'fields': ['id', 'abbr', 'code']})
  courses = {}
  for cur in courses_output:
    courses[cur['abbr']] = {'code':cur['code'] }

  print(f'\033[0;32m[INFO]\033[0m Ciclos:')
  print_dictionary(courses)

  # matriz para comprobar que tareas están creadas y cuales no de cada ciclo
  check_task= {}

  for cur in courses:
    check_task[cur] ={}
    for tk in tasks_keys:
      check_task[cur][tk] = False

  current_classrooms = models.execute_kw(db, uid, password, 'maya_core.classroom', 'search_read', [[]], { 'fields': ['id', 'code']})
  print(f'\033[0;32m[INFO]\033[0m Classroom existentes:')
  print_list(current_classrooms)

  current_tasks = models.execute_kw(db, uid, password, 'maya_core.task_moodle', 'search_read', [[]], { 'fields': ['id', 'key','classroom_id', 'course_abbr']})
  print(f'\033[0;32m[INFO]\033[0m Tareas existentes:')
  print_list(current_tasks)

except (xmlrpc.client.Fault) as e:
  print('\033[0;31m[ERROR]\033[0m ' + e.faultString)
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

line_count_OK = 0
line_count_ERROR = 0

for task in current_tasks:
  check_task[task['course_abbr']][task['key']] = task['classroom_id'][1]

for task in tasks:
  print(f"\033[0;32m[INFO]\033[0m Procesando: {task['description']} / {task['course_abbr']}")

  try:
    # Está en Maya?
    classroom_id = next((classroom for classroom in current_classrooms if classroom['code'] == task['classroom_code']), None)

    if classroom_id == None:
      print(f'    \033[0;31m[ERROR]\033[0m No se encuentra el id del aula {task["classroom_code"]}')
      line_count_ERROR += 1
      continue
    
    task_exist = next((item for item in current_tasks if item['key'] == task['key'] and item['classroom_id'][0] == classroom_id['id']), None)
    
    if task_exist == None: # no está
      if check_task[task["course_abbr"]][task['key']] != False:
        print(f'    \033[0;31m[ERROR]\033[0m Ya existe una tarea para esa key ({task["key"]}) y ese ciclo ({task["course_abbr"]}) en otra aula ({check_task[task["course_abbr"]][task["key"]]})')
        line_count_ERROR += 1
        continue

      task_id = models.execute_kw(db, uid, password, 'maya_core.task_moodle', 'create', [{
          'key': task['key'],
          'description': task['description'],
          'moodle_id': task['moodle_id'],
          'course_abbr': task['course_abbr'],
          'classroom_id': classroom_id['id'] }])
      
      check_task[task["course_abbr"]][task['key']] = classroom_id['code']
      line_count_OK += 1
      
    else: # ya está en Maya
      print(f'   \033[0;32m[INFO]\033[0m {task["key"]}/{task["course_abbr"]} ya existe en Maya. Actualizándolo') 
      
      models.execute_kw(db, uid, password, 'maya_core.task_moodle', 'write', [[task_exist['id']],
           { 'description': task['description'], 
             'course_abbr': task['course_abbr'],
             'moodle_id': task['moodle_id'] }])
      
      check_task[task["course_abbr"]][task['key']] = True
    
      line_count_OK += 1

  except (xmlrpc.client.Fault) as e:
    print('   \033[0;31m[ERROR]\033[0m ' + e.faultString)
    line_count_ERROR += 1
  except KeyError:
    print('   \033[0;31m[ERROR]\033[0m Clave no encontrada.')
    line_count_ERROR += 1

print(f'\033[0;32m[INFO]\033[0m Procesados {line_count_OK} aulas virtuales / Errores: {line_count_ERROR}.')

print(f'\033[0;32m[INFO]\033[0m Tabla de tareas creadas (\033[0;32mO\033[0m) / por crear (\033[0;31mX\033[0m)')

header_table = '       {:<12}'.format('CICLO')
for ky in tasks_keys:
  header_table += ' {:^12}'.format(ky)

print(header_table)
print('      ' + '-' * (len(header_table) - 6))
for key, value in check_task.items():
  row = '        {:<12}'.format(key)
  for vl in value.values():
    if vl == False:
      # dejo 24 de espacio ya que los caracteres del color ANSI, aunque no se ven cuentan
      row += '{:^24}'.format('\033[0;31mX\033[0m')
    else:
      row += '{:^24}'.format('\033[0;32mO\033[0m')
  print(row)

