# -*- coding: utf-8 -*-
{
    'name': "Maya | Core",
    'version': '0.1.0a',

    'summary': """
        Módulo (Core) para la gestión interna del CEED (Ciclos Formativos)""",

    'description': """
        Módulo que simplifica y automatiza el trabajo de un centro de Ciclos Formativos a distancia.
        Implementa la funcionalidad básica que será utilizada por otras extensiones como:
         - Maya | Convalidaciones: gestión de las convalidaciones,
         - Maya | PFC: gestión del Proyecto Fin de Ciclo

        Este módulo permite entre otras cosas
         - Control de profesores y sus roles
         - Control de ciclos y módulos
         - Generación automática de calendiario escolar
         - Gestión de las aulas virtuales
         - Gestión de las tareas automatizadas (CronJobs)
         ...
    """,

    'website': "https://portal.edu.gva.es/ceedcv/",
    'author': 'Alfredo Oltra',
    'maintainer': 'Alfredo Oltra <alfredo.ptcf@gmail.com>',
    'company': '',
    'category': 'Productivity',

    'license': 'AGPL-3',
    # precio del módulo
    'price': 0,

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # external dependencies that have to be installed. Can be python or bin dependencies
    # Only checks whether the dependency is installed. Not install the dependency!!
    'external_dependencies': {
       'python': ['moodleteacher', 'toolz'],
    },
    # always loaded
    'data': [
        # seguridad
        'security/security_groups.xml',
        'security/core_access.xml',
        'security/cron_access.xml',
        'security/ir.model.access.csv',
        # vistas
        'views/views.xml',
        'views/config_settings_view.xml',
        'views/templates.xml',
        # datos de modelos
        'data/config/config_data.xml',
        'data/school.xml',
        'data/departaments.xml',
        'data/courses.xml',
        'data/subjects/aig.xml',
        'data/subjects/tic.xml',
        'data/subjects/hit.xml',
        'data/subjects/cim.xml',
        'data/subjects/common.xml',
        'data/roles/headquarters.xml',
        'data/roles/tutors.xml',
        'data/registered_cron_jobs.xml',
        # reports
        'reports/custom_footer.xml',
        'reports/school_calendar.xml',
        'reports/paper_format.xml',  
    ],
    'installable': True,
    'application': True,
}