from ..globals import globals
from argparse import ArgumentParser
from pathlib import Path
from dirsync import sync
from shutil import copyfile
import PyInstaller.__main__
import sys


#TODO reprogramm this class > method for every condition in arg switch > classmethod for every helper function
class Decore_prompt(object):
    def __init__(self):
        self.parser = ArgumentParser()
        
        self.parser.add_argument('--prepare', action='store_true', help='Prepare decore Base application with helper files to get startet')
        self.parser.add_argument('--sample', action='store_true', help='Copy the "decore Base" sample application to project root folder')
        self.parser.add_argument('--dev', action='store_true', help='Run decore Base application in development mode')
        self.parser.add_argument('--build', action='store_true', help='Build decore Base application for production')
        self.args, t_unknown_args = self.parser.parse_known_args()

        if not t_unknown_args:
            if self.args.prepare:
                self.copy_launch()
                self.copy_gitignore()
                self.sync_spa()
                self.create_bases()
                exit()
            elif self.args.sample:
                if not globals.config.app_id == '364871e4-6727-4e1f-80a2-acc9c83ace92':
                    self.sync_sample()
                    exit()
                else:
                    raise Exception('You can not use the "sample" command in sample project context')
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
            exit()


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

    def sync_sample(self):
        t_sample_source = Path(__file__).parent.parent.joinpath('sample')
        t_sample_destination = Path('sample')
        t_sample_destination.mkdir(parents=True, exist_ok=True)
        sync(str(t_sample_source.absolute()), str(t_sample_destination.absolute()), 'sync', purge=True)
    
    def create_bases(self):
        t_bases_init_path = Path('bases').joinpath('__init__.py')
        if not t_bases_init_path.exists():
            t_bases_init_path.parent.mkdir(parents=True, exist_ok=True)
            with open(t_bases_init_path, 'w'): pass