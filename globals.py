from .classes.global_prompt import Global_prompt

from pathlib import Path
from pykeepass import create_database, PyKeePass
from uuid import uuid4
import json,logging
from dirsync import sync
from shutil import copyfile

logging.basicConfig(format='[%(levelname)s] | %(message)s', level=logging.INFO)

class Global_flags(object):
    def __init__(self):
        self.purge_unused_database_cols = None

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
        self.prompt = Global_prompt()
        #TODO - move to model
        self.kdb = self.get_kdb()

        if self.prompt.args.cmd == 'prepare':
            self.copy_launch()
            self.sync_spa()
            exit()
        elif self.prompt.args.cmd == 'dev':
            self.flags.purge_unused_database_cols = False
        else:
            self.flags.purge_unused_database_cols = True

    def copy_launch(self):
        t_prepare_path = Path(__file__).parent.joinpath('prepare')
        t_launch_source = t_prepare_path.joinpath('.vscode').joinpath('launch.json')
        t_launch_destination = Path('.vscode').joinpath('launch.json')
        t_launch_destination.parent.mkdir(parents=True, exist_ok=True)
        copyfile(str(t_launch_source.absolute()), str(t_launch_destination.absolute()))
            

    def sync_spa(self):
        t_prepare_path = Path(__file__).parent.joinpath('prepare')
        t_spa_source = t_prepare_path.joinpath('spa')
        t_spa_destination = Path('spa')
        t_spa_destination.mkdir(parents=True, exist_ok=True)
        sync(str(t_spa_source.absolute()), str(t_spa_destination.absolute()), 'sync', purge=True)
        

    #TODO - move to model
    def get_kdb(self):
        t_kdp_path = Path().joinpath(self.config.state_path).joinpath('keybase.kdbx')
        t_kdp_path.parent.mkdir(parents=True, exist_ok=True)
        if not t_kdp_path.exists():
            create_database(str(t_kdp_path.absolute()), password='12345678')
        return PyKeePass(str(t_kdp_path.absolute()), password='12345678')
    
globals = Globals()