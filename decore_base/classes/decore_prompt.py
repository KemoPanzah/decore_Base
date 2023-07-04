from ..globals import globals
from argparse import ArgumentParser
from pathlib import Path
from dirsync import sync
from shutil import copyfile
import PyInstaller.__main__


#TODO reprogramm this class > method for every condition in arg switch > classmethod for every helper function
class Decore_prompt(object):
    def __init__(self):
        self.parser = ArgumentParser()
        
        self.parser.add_argument('--prepare', action='store_true', help='Prepare decore Base application with helper files to get startet')
        self.parser.add_argument('--dev', action='store_true', help='Run decore Base application in development mode')
        self.parser.add_argument('--build', action='store_true', help='Build decore Base application for production')
        self.args, t_unknown_args = self.parser.parse_known_args()

        if not t_unknown_args:
            if self.args.prepare:
                self.copy_launch()
                self.copy_gitignore()
                self.sync_spa()
                self.create_base_dir()
                self.create_model_dir()
                exit()
            elif self.args.dev:
                globals.flags.purge_unused_database_cols = False
                globals.flags.dev_mode = True
                self.sync_spa()
            elif self.args.build:
                PyInstaller.__main__.run([
                    '--paths="."',
                    '--add-data=spa;spa',
                    '--collect-data=pykeepass',
                    'app.py'
                ])
            else:
                pass
        else:
            print('Unknown arguments: ' + str(t_unknown_args) + ' Use --help for more information')


    def copy_launch(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_launch_source = t_prepare_path.joinpath('.vscode').joinpath('launch.json')
        t_launch_destination = Path('.vscode').joinpath('launch.json')
        t_launch_destination.parent.mkdir(parents=True, exist_ok=True)
        copyfile(str(t_launch_source.absolute()), str(t_launch_destination.absolute()))

    def copy_gitignore(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_gitignore_source = t_prepare_path.joinpath('.gitignore')
        t_gitignore_destination = Path('.gitignore')
        copyfile(str(t_gitignore_source.absolute()), str(t_gitignore_destination.absolute()))
            
    def sync_spa(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_spa_source = t_prepare_path.joinpath('spa')
        t_spa_destination = Path('spa')
        t_spa_destination.mkdir(parents=True, exist_ok=True)
        sync(str(t_spa_source.absolute()), str(t_spa_destination.absolute()), 'sync', purge=True)

    def create_base_dir(self):
        t_bases_init_path = Path('bases').joinpath('__init__.py')
        if not t_bases_init_path.exists():
            t_bases_init_path.parent.mkdir(parents=True, exist_ok=True)
            with open(t_bases_init_path, 'w'): pass

    def create_model_dir(self):
        t_models_init_path = Path('models')
        if not t_models_init_path.exists():
            t_models_init_path.mkdir(parents=True, exist_ok=True)