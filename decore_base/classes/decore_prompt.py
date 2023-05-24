from ..globals import globals
from argparse import ArgumentParser
from pathlib import Path
from dirsync import sync
from shutil import copyfile

class Decore_prompt(object):
    def __init__(self):
        self.parser = ArgumentParser()
        self.cmd = self.parser.add_subparsers(dest='cmd')
        self.prepare = self.cmd.add_parser('prepare', help='Prepare decore App with helping files to get startet')
        self.sample = self.cmd.add_parser('sample', help='Copy the "decore Base" sample application to project root folder')
        self.dev = self.cmd.add_parser('dev', help='Run decore App in Development mode')
        # self.create = self.cmd.add_parser('create', help='create')
        # self.create.add_argument('-t', '--type', type=str, choices=['base', 'model'], required=True, help='choose your type')
        # self.create.add_argument('-i', '--id', type=str, required=True)
        # self.create.add_argument('-p', '--parent', type=str, required=False)
        self.args = self.parser.parse_args()

        if self.args.cmd == 'prepare':
            self.copy_launch()
            self.copy_gitignore()
            self.sync_spa()
            self.create_bases()
            exit()
        elif self.args.cmd == 'sample':
            if not globals.config.app_id == '364871e4-6727-4e1f-80a2-acc9c83ace92':
                self.sync_sample()
                exit()
            else:
                raise Exception('You can not use the "sample" command in sample project context')
        elif self.args.cmd == 'dev':
            self.sync_spa()
            globals.flags.purge_unused_database_cols = False
        else:
            pass

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