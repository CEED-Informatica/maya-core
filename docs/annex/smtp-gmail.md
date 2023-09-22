---
layout: page
menubar: annex
title: Configuración gmail como SMTP 
subtitle: Anexos
show_sidebar: false
hero_height: is-fullwidth
---

## Configuración de _gmail_ como servidor de correo saliente

> como ejemplo se supone que la cuenta a usar es _mi_correo@gmail.com_.

1. [ ] Activar la autenticación en dos pasos en _gmail_.

   > Si el correo pertenece a una organización es necesario que sea el administrador de la organización el que visualice la opción para el usuario.

2. [ ] Generar una contraseña para la aplicación.

   Crear una nueva contraseña asignado como nombre de la app _Maya_. La contraseña que nos proporciona es la que hay que introducir en el proceso de configuración del servidor de correo saliente.

3. [ ] Configurar un servidor de correo saliente:

    Como _administrador_ acceder en Odoo:

       Ajustes / Ajustes generales / Servidores de correo externo / Servidor de correo saliente

      con los parámetros:

      | SMTP Server | SMTP Port | Connection Security | Username | Password |
      | :---------: | :-------: | :-----------------: | :------: | :------: |
      | smtp.gmail.com | 465 | SSL/TLS | mi_correo@gmail.com | contraseña obtenida en el paso 2 | 