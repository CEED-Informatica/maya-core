## Conexión Maya &harr; Moodle

> A lo largo del documento, el prompt **$** indica un comando a introducir en el host, mientras que el prompt **>** indica un comando a introducir en el contenedor. Además, **[PWD_MODULO]** indica el directorio raíz del módulo.
### Creación del token de comunicación

1. [ ] Configurar el fichero _[PWD_MODULO]/misc/scripts/save_token_moodle/moodle_host.txt_ con la url del servidor de Moodle.

    > En el caso de trabajar con el servicio Moodle que proporcina _odoodock_, la url es el nombre del servicio: _http://moodle:8080_ . 

    En el caso de estar trabajando con _odoodock_ hay que modificar el fichero desde dentro del contenedor:

    ```
    $ docker exec -it odoodock-web-1 bash
    > cd /mnt/extra-addons/misc/scripts/save_token_moodle
    > nano moodle_host.txt
    ```
2. [ ] Dar permisos de ejecución al script.

    ```
    cd [PWD_MODULO]/misc/scripts/create_users/
    chmod +x save_token_moodle.py
    ```

    o, si se trabaja con _odoodock_:

    ```
    > chmod +x save_token_moodle.py
    ```

3. [ ] Ejecutar el script

    ```
    ./save_token_moodle.py
    ```

    o, si se trabaja con _odoodock_:

    ```
    > ./save_token_moodle.py
    ```

    con los parámetros:

    * Usuario: usuario de referencia para que **Maya** lea sus credenciales. Ha de ser el mismo que el que se configura en los ajustes de _Odoo_ como usuario. **Maya** permite que existan varias opciones (varias usuarios) que se conectan a Moodle. Este usuario funciona a modo de clave para saber que usuario de moodle y contraseña se va a utilizar. Es muy habitual que sea _maya_
    * Usuario _Moodle_: usuario de _Moodle_ que relizará las gestiones. Ver apartado 3 del documento [moodle-config](/maya-core/docs/como-empezar/moodle-config). Tiene que tener asignado el rol profesor.
    * Contraseña del usuario _Moodle_

### Creación de las aulas virtuales

### Creación de tareas