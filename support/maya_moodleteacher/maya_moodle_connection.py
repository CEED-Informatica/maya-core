# -*- coding: utf-8 -*-
import os
import pickle
from moodleteacher.connection import MoodleConnection  

import logging

_logger = logging.getLogger(__name__)

class MayaMoodleConnection(MoodleConnection):
  """
    Configura una conexión a un ser servidor de Moodle a partir
    de los datos almacenados en ~/.maya_moodleteacher.

    Hereda de MoodleConnection 
    
    Args:
      moodle_host:        La URL base del servidor de Moodle
      user:               Usuario Moodle que realiza la conexión
  """
  def __init__(self, moodle_user, moodle_host):

    if not moodle_host or not moodle_user:
      raise AttributeError('No se ha proporcionado usuario o url.')
    
    try:
      with open(os.path.expanduser("~/.maya_moodleteacher"), "rb") as f:
        users_tokens = pickle.load(f)
    except Exception:
      raise Exception('No se encuentra el fichero .maya_moodleteacher. Utiliza el script save_token_moodle para generarlo.')
  
    if moodle_user not in users_tokens:
      raise Exception('El usuario {} no se encuentra en el fichero .maya_moodleteacher. Utiliza el script save_token_moodle para añadirlo.'.format(moodle_user))
  

    super().__init__(moodle_host,  str(users_tokens[moodle_user]), is_fake = False)
    