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

def link_subject_course_classroom(course, subject, classroom) -> int:
  """ 
  Enlaza el módulo con el aula virtual para cada ciclo 
  Devuelve el id de Odoo de la tupla creada
  """
  return models.execute_kw(db, uid, password, 'maya_core.subject_classroom_rel', 'create', [{
        'course_id': course,
        'subject_id': subject,
        'classroom_id': classroom
        }])

print('\033[1mMaya | create-classrooms. v1.1\033[0m')

parser = argparse.ArgumentParser(
  description = 'Crea aulas virtuales (Maya) desde un csv')

# argumentos
parser.add_argument('csv_filename', help = 'Fichero csv con los datos: id,code,description,lang') 
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

classrooms = []

try:
  # end point xmlrpc/2/common permite llamadas sin autenticar
  print('\033[0;32m[INFO]\033[0m Conectando con',url, ' -> ', db)
  common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
  print('\033[0;32m[INFO]\033[0m Odoo server', common.version()['server_version'])
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print('\033[0;31m[ERROR]\033[0m Compruebe que el servidor de Odoo esté arrancado')
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

# autenticación
uid = common.authenticate(db, username, password, {})

with open(sys.argv[1]) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter = ',')
  line_count = 0
  for row in csv_reader:
    if line_count > 0:
      classrooms.append({
          'code': row[1],
          'description': row[2],
          'moodle_id': row[0],
          'lang_id': row[3]
      })
    line_count += 1

print('\033[0;32m[INFO]\033[0m Aulas en csv:', len(classrooms))    

try:
  models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

  # obtengo todos los ciclos
  courses_output = models.execute_kw(db, uid, password, 'maya_core.course', 'search_read', [[]], { 'fields': ['id', 'code', 'abbr', 'name']})
  courses = {}
  for cur in courses_output:
    courses[cur['code']] = {'id': cur['id'], 'abbr':cur['abbr'], 'name': cur['name']  }

  print(f'\033[0;32m[INFO]\033[0m Ciclos:')
  print_dictionary(courses)

  # obtengo todos los módulos
  subjects_output = models.execute_kw(db, uid, password, 'maya_core.subject', 'search_read', [[]], { 'fields': ['id', 'code', 'abbr', 'name']})
  subjects = {}
  for sub in subjects_output:
    subjects[sub['code']] = {'id': sub['id'], 'abbr':sub['abbr'],  }

  print(f'\033[0;32m[INFO]\033[0m Módulos:')
  print_dictionary(subjects)

  # idiomas activos
  languages_output = models.execute_kw(db, uid, password, 'res.lang', 'search_read', [[['active','=', True]]], { 'fields': ['id','code']})
  languages = []
  for lang in languages_output:
    languages.append(lang['code'])

  print(f'\033[0;32m[INFO]\033[0m Idiomas:')
  print_list(languages_output)

  # aulas virtuales que ya existen en Maya, para poder actualizar o crear de cero
  current_classrooms = models.execute_kw(db, uid, password, 'maya_core.classroom', 'search_read', [[]], { 'fields': ['id', 'code']})
  print(f'\033[0;32m[INFO]\033[0m Classroom existentes:')
  print_list(current_classrooms)

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

for classroom in classrooms:
  print("\033[0;32m[INFO]\033[0m Procesando ", classroom['code'])
  try:
    # si el idioma del aula no está configurado asigno uno por defecto
    if classroom['lang_id'] not in languages:
      print(f'   \033[0;31m[ERROR]\033[0m ({classroom["code"]}) {classroom["lang_id"]} no existe o no está activo en Maya. Asignando idioma por defecto {languages[0]}.')
      classroom['lang_id'] = languages[0]

    # ide del idioma
    classroom_lang = next((lang['id'] for lang in languages_output if lang['code'] == classroom['lang_id']),None)

    # Existe ya Maya?
    classroom_exist = next((item for item in current_classrooms if item['code'] == classroom['code']), None)
    
    code_blocks = classroom['code'].split('_')
    classroom['description'] = f'Aula de {classroom["description"]} ({courses[code_blocks[-2]]["abbr"]})' 

    if classroom_exist == None: # no está ya en Maya 
      classroom['lang_id'] = classroom_lang  
      classroom_id = models.execute_kw(db, uid, password, 'maya_core.classroom', 'create', [classroom])
    else: # ya está en Maya
      print(f'   \033[0;32m[INFO]\033[0m {classroom["code"]} ya existe en Maya. Actualizándolo')

      models.execute_kw(db, uid, password, 'maya_core.classroom',
                                           'write', 
                                           [[classroom_exist['id']],
                                           {'description': classroom['description'], 
                                            'lang_id': classroom_lang,
                                            'moodle_id': classroom['moodle_id']}])
      
      classroom_id = classroom_exist['id']
    
    # relación con módulos
    if code_blocks[-1] == 'TU02CF' or code_blocks[-1] == 'TU01CF':  # en versiones anteriores de aules se nombraban así
    # if code_blocks[-1] == 'TUT0':  # aula de tutoria común para primero y segundo 
      link_subject_course_classroom(courses[code_blocks[-2]]['id'], subjects['TUT1']['id'], classroom_id)
      print(f'   \033[0;32m[INFO]\033[0m Asociado {classroom["code"]} con el módulo {subjects["TUT1"]["abbr"]} en {courses[code_blocks[-2]]["abbr"]}')
      link_subject_course_classroom(courses[code_blocks[-2]]['id'], subjects['TUT2']['id'], classroom_id)
      print(f'   \033[0;32m[INFO]\033[0m Asociado {classroom["code"]} con el módulo {subjects["TUT2"]["abbr"]} en {courses[code_blocks[-2]]["abbr"]}')
    else:
      link_subject_course_classroom(courses[code_blocks[-2]]['id'], subjects[code_blocks[-1]]['id'], classroom_id)
      print(f'   \033[0;32m[INFO]\033[0m Asociado {classroom["code"]} con el módulo {subjects[code_blocks[-1]]["abbr"]} en {courses[code_blocks[-2]]["abbr"]}')

    line_count_OK += 1

  except (xmlrpc.client.Fault) as e:
    print('   \033[0;31m[ERROR]\033[0m ' + e.faultString)
    line_count_ERROR += 1
  except KeyError:
    print('   \033[0;31m[ERROR]\033[0m Clave no encontrada.')
    line_count_ERROR += 1

print(f'\033[0;32m[INFO]\033[0m Procesados {line_count_OK} aulas virtuales / Errores: {line_count_ERROR}.')
print(f'\033[0;32m[INFO]\033[0m Hay que repasar y asignar las aulas de inglés técnico con los módulos correspondientes.')