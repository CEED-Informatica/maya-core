---
layout: page
menubar: docs_menu
title: Instalación Maya | Core
subtitle: Cómo empezar
show_sidebar: false
hero_height: is-fullwidth
---

## Instalación Maya | Core

> Se parte de la clonación del módulo en la carpeta donde se ubican las addons, tal y como se explica en configuración de Odoo.

> A lo largo del documento, el prompt **$** indica un comando a introducir en el host, mientras que el prompt **>** indica un comando a introducir en el contenedor.

1. [] Instalar los requerimientos. Desde la carpeta del módulo clonado, _maya_core_, ejecutar:

   ```
   $ pip3 install -r requirements-dev.txt
   ```

   En caso de usar [odooddock](https://aoltra.github.io/odoodock/), hay que entrar dentro del contendor y ejecutar el comando:

   ```
   $ docker exec -it odoodock-web-1 bash
   > pip3 install -r requirements-dev.txt
   ```

  > En caso de realizar una instalación

2. [] Instalar **Maya | Core**

