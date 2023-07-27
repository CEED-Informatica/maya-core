# -*- coding: utf-8 -*-
{
    'name': "maya | Core",
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
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/courses.xml'
    ],
    'installable': True,
    'application': True,
}