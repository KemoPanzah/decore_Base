from pathlib import Path
from dirsync import sync
from shutil import copyfile

class Decore_prepare:
    
    def run(self, dev=True):
        self.copy_launch()
        self.sync_spa()
        self.sync_pwa()
        self.sync_bases()
        self.sync_models()
    
    def set_gitignore(self, p_path: str):
        t_gitignore_path = Path(p_path).joinpath('.gitignore')
        if not t_gitignore_path.exists():
            with open(t_gitignore_path, 'w') as f:
                f.write('*\n')
               
    def copy_launch(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_launch_source = t_prepare_path.joinpath('.vscode').joinpath('launch.json')
        t_launch_destination = Path('.vscode').joinpath('launch.json')
        t_launch_destination.parent.mkdir(parents=True, exist_ok=True)
        copyfile(str(t_launch_source.absolute()), str(t_launch_destination.absolute()))
        
    def sync_spa(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_spa_source = t_prepare_path.joinpath('spa')
        t_spa_destination = Path('spa')
        t_spa_destination.mkdir(parents=True, exist_ok=True)
        sync(str(t_spa_source.absolute()), str(t_spa_destination.absolute()), 'sync', purge=True)
        self.set_gitignore(t_spa_destination)

    def sync_pwa(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_pwa_source = t_prepare_path.joinpath('pwa')
        t_pwa_destination = Path('pwa')
        t_pwa_destination.mkdir(parents=True, exist_ok=True)
        sync(str(t_pwa_source.absolute()), str(t_pwa_destination.absolute()), 'sync', purge=True)
        self.set_gitignore(t_pwa_destination)

    def sync_bases(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_bases_source = t_prepare_path.joinpath('bases')
        t_bases_destination = Path('bases')
        if not t_bases_destination.exists():
            t_bases_destination.mkdir(parents=True, exist_ok=True)
            sync(str(t_bases_source.absolute()), str(t_bases_destination.absolute()), 'sync', purge=True)

    def sync_models(self):
        t_prepare_path = Path(__file__).parent.parent.joinpath('prepare')
        t_models_source = t_prepare_path.joinpath('models')
        t_models_destination = Path('models')
        if not t_models_destination.exists():
            t_models_destination.mkdir(parents=True, exist_ok=True)
            sync(str(t_models_source.absolute()), str(t_models_destination.absolute()), 'sync', purge=True)