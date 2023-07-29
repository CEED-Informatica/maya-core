#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import csv
import sys, argparse

def print_dictionary(dictionary):
  for key, value in dictionary.items():  
    print(' * {} ({})'.format(key, value))

def print_list(list):
  for value in list:  
       print(' * {}'.format(value))

print('\033[1mMaya | create-users. v1.1\033[0m')

parser = argparse.ArgumentParser(
  description = 'Crea usuarios (Odoo) y empleados (Maya) desde un csv')

# argumentos
parser.add_argument('csv_filename', help = 'Fichero csv con los datos: name,surname,email,lang,dep,type') 
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

users = []
employees = {}

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

with open(args.csv_filename) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter = ',')
  line_count = 0
  for row in csv_reader:
    if line_count > 0:
      users.append({
          'name': '%s %s' % (row[0], row[1]),
          'login': row[2],
          'lang': row[3],
          'company_ids':[1],
          'company_id': 1,
          'email': row[2]
          # 'new_password': el password no se inserta por motivos de seguridad
      })
      employees[row[2]] = { 'name': row[0],
          'surname': row[1],
          'employee_type': row[5],
          'departament_ids': row[4]
      }
    line_count += 1

print('\033[0;32m[INFO]\033[0m Usuarios en csv:', len(users))    

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# obtengo todos los departamentos
try:
  departaments_output = models.execute_kw(db, uid, password, 'maya_core.departament', 'search_read', [[]], { 'fields': ['id', 'name']})
  departaments = {}
  for dep in departaments_output:
    departaments[dep['name']] = dep['id']

  print(f'\033[0;32m[INFO]\033[0m Departamentos:')
  print_dictionary(departaments)

  # idiomas activos
  languages_output = models.execute_kw(db, uid, password, 'res.lang', 'search_read', [[['active','=', True]]], { 'fields': ['code']})
  languages = []
  for lang in languages_output:
    languages.append(lang['code'])

  print(f'\033[0;32m[INFO]\033[0m Idiomas:')
  print_list(languages_output)
except Exception as e:
  print('\033[0;31m[ERROR]\033[0m ' + str(e))
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

# obtengo la categoria Maya
maya_id_category = models.execute_kw(db, uid, password, 'ir.module.category', 
                                     'search_read', [[['name','=', 'Maya']]], { 'fields': ['id']})

# obtengo todos los grupos
teacher_group = models.execute_kw(db, uid, password, 'res.groups', 'search_read', 
                                  [[['category_id','=', maya_id_category[0]['id']], 
                                    ['name','=', 'Profesorado']]]) 
admin_group = models.execute_kw(db, uid, password, 'res.groups', 'search_read', 
                                [[['category_id','=', maya_id_category[0]['id']], 
                                  ['name','=', 'Administración (secretaria)']]]) 

print(f'\033[0;32m[INFO]\033[0m Grupos:')
print(f' * Profesorado ({teacher_group[0]["id"]})')
print(f' * Secretaría ({admin_group[0]["id"]})')

groups = {}
groups['profesor'] = teacher_group[0]
groups['pas'] = admin_group[0]

try:
  inactive_users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['active','=', False]]], { 'fields': ['id', 'login']})
  print(f'\033[0;32m[INFO]\033[0m Usuarios inactivos:')
  print_list(inactive_users)
except (xmlrpc.client.Fault) as e:
  print('\033[0;31m[ERROR]\033[0m ' + e.faultString)
  print(f'\033[0;32m[INFO]\033[0m Saliendo...')
  exit()

line_count_OK = 0
line_count_ERROR = 0

for user in users:  
  print("\033[0;32m[INFO]\033[0m Procesando ", user)
  try:
    if user['lang'] not in languages:
      print(f'   \033[0;33m[AVISO]\033[0m ({user["login"]}) {user["lang"]} no existe o no está activo en Maya. Asignando idioma por defecto {languages[0]}.')
      user['lang'] = languages[0]

    # Esta en Maya pero esta inactivo
    odoo_user = next((item for item in inactive_users if item['login'] == user['login']), None)
    
    if odoo_user == None: # no está inactivo en Maya 
      # se crea. En caso de que ya exista salta una excepción
      id = models.execute_kw(db, uid, password, 'res.users', 'create', [user])
      employees[user['login']]['user_id'] = id
      employees[user['login']]['departament_ids'] = [(4, departaments[employees[user['login']]['departament_ids']])]
      models.execute_kw(db, uid, password, 'maya_core.employee', 'create', [employees[user['login']]])

      models.execute_kw(db, uid, password, 'res.users', 'write', [id, {'groups_id': [(4, groups[employees[user['login']]['employee_type']]['id'])] }])

    else: # está pero inactivo
      print(f'   \033[0;32m[INFO]\033[0m {user["name"]} ({user["login"]}) ya existe en Maya. Activándolo')
      models.execute_kw(db, uid, password, 'res.users', 'write', [[odoo_user['id']], {'active': True}])
      models.execute_kw(db, uid, password, 'res.users', 'write', [[odoo_user['id']], {'groups_id': [(4, groups[employees[user['login']]['employee_type']]['id'])] }])
   
    line_count_OK += 1
  except (xmlrpc.client.Fault) as e:
    print('   \033[0;31m[ERROR]\033[0m ' + e.faultString)
    line_count_ERROR += 1
  except KeyError:
    print('   \033[0;31m[ERROR]\033[0m Clave no encontrada. Posiblemente el departamento no existe')
    line_count_ERROR += 1

print(f'\033[0;32m[INFO]\033[0m Procesados {line_count_OK} usuarios / Errores: {line_count_ERROR}.')


