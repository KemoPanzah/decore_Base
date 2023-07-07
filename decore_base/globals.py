from pathlib import Path
from uuid import uuid4
import json,logging,sys

from .classes.globals_keybase import Global_keybase

logging.basicConfig(format='[%(levelname)s] | %(message)s', level=logging.INFO)

class Global_flags(object):
    def __init__(self):
        self.production_mode = self.set_production_mode()
        self.dev_mode = False
        self.purge_unused_database_cols = False
    
    def set_production_mode(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return True
        else:
            return False

class Global_config(object):
    def __init__(self):
        self.__data__ = {   
                        'default': {'app_id': str(uuid4()), 'app_port': 5555, 'state_path': 'state'}, 
                        'remote': {'server_addr': '0.0.0.0', 'server_port': 51515}
                        }
        self.load()

    def load(self):
        try:
            with open('config.json') as t_file:
                self.__data__ = json.load(t_file)
        except FileNotFoundError:
            with open('config.json', 'w') as t_file:
                json.dump(self.__data__, t_file, default=str, indent=4)

    @property
    def app_id(self):
        return self.__data__['default']['app_id']

    @property
    def app_port(self):
        return self.__data__['default']['app_port']

    @property
    def state_path(self):
        return self.__data__['default']['state_path']

    @property
    def server_addr(self):
        return self.__data__['remote']['server_addr']

    @property
    def server_port(self):
        return self.__data__['remote']['server_port']

class Globals(object):
    def __init__(self):
        self.flags = Global_flags()
        self.config = Global_config()
        self.keybase = Global_keybase(Path().joinpath(self.config.state_path).joinpath('keybase.kdbx'))

globals = Globals()
