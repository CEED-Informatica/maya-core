---
layout: page
menubar: docs_menu
title: Configuración Maya | Core
subtitle: Cómo empezar
show_sidebar: false
hero_height: is-fullwidth
---

## Configuración Maya | Core

1. [ ] Configurar correo saliente. SMTP
  
      Como _administrador_ acceder en Odoo:

         Ajustes / Ajustes generales / Servidores de correo externo / Servidor de correo saliente

      Una configuración habitual puede ser la de usar una cuenta de _gmail_ como servidor de correo saliente. Ver [configurar SMTP gmail]((/maya-core/annex/smtp-gmail)) 

2. [ ] Personalizar la empresa. Por defecto **Maya | Core** se configura con los datos del CEEDCV. Para modificarlos e indicar los datos del centro hay que acceder como _administrador_:

         Ajustes / Ajustes generales / Empresas / Actualizar información

3. [ ] Asignar la url base. 
    
    En el caso de que se acceda desde una red local, o se utiliza un DNS local o se modifica el fichero _C:\windows\system32\drivers\etc\host_ (Windows) o _/etc/hosts_ (Linux/MacOS) de **todos** los ordenadores que tienen acceso al servidor para incluir su nombre. Para asignarlo en Odoo, hay que acceder como _administrador_ y en modo _debug_ a:
  
         Ajustes / Técnicos / Parámetros / Parámetros de sistema / web.base.url

    Si el servidor va a estar disponible a través de internet (con un dominio ya asignado), únicamente indicarlo en la ruta anterior.

    > Odoo podría cambiar de manera automática el valor de _web.base.url_ en el caso de que algún cliente realizará el acceso mediante otra url (IP, localhost)


4. [ ] Creación de usuarios
