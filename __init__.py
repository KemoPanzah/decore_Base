from .globals import globals
from .decore import decore
#from .library import *

from importlib import util
from pathlib import Path
from io import open

t_bases_init_path = Path('bases').joinpath('__init__.py')

if not t_bases_init_path.exists():
    t_bases_init_path.parent.mkdir(parents=True, exist_ok=True)
    with open(t_bases_init_path, 'w'): pass

spec = util.spec_from_file_location('bases', t_bases_init_path)
module = util.module_from_spec(spec)
spec.loader.exec_module(module)