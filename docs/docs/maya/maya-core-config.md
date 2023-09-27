---
layout: page
menubar: docs_menu
title: Configuración Maya | Core
subtitle: Cómo empezar
show_sidebar: false
hero_height: is-fullwidth
---

## Configuración Maya | Core

> A lo largo del documento, el prompt **$** indica un comando a introducir en el host, mientras que el prompt **>** indica un comando a introducir en el contenedor. Además, **[PWD_MODULO]** indica el directorio raíz del módulo.

1. [ ] Configurar correo saliente. SMTP
  
      Como _administrador_ acceder en Odoo:

         Ajustes / Ajustes generales / Servidores de correo externo / Servidor de correo saliente

      Una configuración habitual puede ser la de usar una cuenta de _gmail_ como servidor de correo saliente. Ver [configurar SMTP gmail](/maya-core/annex/smtp-gmail) 

2. [ ] Personalizar la empresa (el centro). Por defecto **Maya | Core** se configura con los datos del CEEDCV. Para modificarlos e indicar los datos del centro hay que acceder como _administrador_ a:

         Ajustes / Ajustes generales / Empresas / Actualizar información

3. [ ] Añadir el logo del centro. Como _administrador_ acceder a:

         Ajustes / Ajustes generales / Empresas / Actualizar información / Añadir Logo

      > Es aconsejable que el logo este en formato png con fondo transparente.


4. [ ] Modificar el favicon. Como _administrador_ acceder a:

         Ajustes / Ajustes generales / Empresas / Actualizar información / MOdificar favicon

      > Es aconsejable un tamaño de 32x32

5. [ ] Asignar la url base. 
    
    En el caso de que se acceda desde una red local, o se utiliza un DNS local o se modifica el fichero _C:\windows\system32\drivers\etc\host_ (Windows) o _/etc/hosts_ (Linux/MacOS) de **todos** los ordenadores que tienen acceso al servidor para incluir su nombre. Para asignarlo en _Odoo_, hay que acceder como _administrador_ y en modo _debug_ a:
  
         Ajustes / Técnicos / Parámetros / Parámetros de sistema / web.base.url

    Si el servidor va a estar disponible a través de internet (con un dominio ya asignado), únicamente indicarlo en la ruta anterior.

    > _Odoo_ podría cambiar de manera automática el valor de _web.base.url_ en el caso de que algún cliente realizará el acceso mediante otra url (IP, localhost), por lo que una vez configurada la url base todos los usuarios deberían acceder a través de ella.

6. [ ] Asignar la url de los informes. 

      Como _administrador_ y en modo _debug_ acceder a:

         Ajustes / Técnicos / Parámetros / Parámetros de sistema 

      Crear un nuevo parámetro llamado _report.url_ y asignarle el valor _http://0.0.0.0:8069_

7. [ ] Creación de usuarios

    Utilizando de plantilla el fichero _[PWD_MODULO]/misc/scripts/users_demo.csv_ añadir todos los usuarios del sistema para posteriormente incorporarlos a **Maya** mediante el script _[PWD_MODULO]/misc/scripts/create_users/create_users.py_

    ```
    cd [PWD_MODULO]/misc/scripts/create_users/
    chmod +x create_users.py
    ./create_users.py -sr USERADMIN -ps PASSADMIN -db NOMDB FICHERO.csv 
    ```
    donde: 

      * USERADMIN: usuario administrador.
      * PASSADMIN: pasword del usuario administrador.
      * NOMDB: es el nombre de la base de datos. 
      * FICHERO.csv: fichero con los datos de los usuarios.

    En el caso de estar trabajando con [odoodock](https://aoltra.github.io/odoodock/) hay que ejecutar el script desde dentro del contenedor:

    ```
    $ docker exec -it odoodock-web-1 bash
    > cd /mnt/extra-addons/misc/scripts/create_users
    > chmod +x create_users.py
    > ./create_users.py -sr USERADMIN -ps PASSADMIN -db NOMDB FICHERO.csv 
    ```

    > El script _create_users.py_ dispone de más opciones que pueden ser consultadas mediante el parámetro _-h_

    > El script detecta si los usuarios ya existen y los mantiene, por lo que puede ser ejecutado multiples veces para añadir a nuevos usuarios.