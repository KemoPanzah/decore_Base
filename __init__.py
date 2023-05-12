from .globals import globals
from .decore import decore
#from .library import *

from importlib import util
from pathlib import Path
from io import open
import logging

try:
    t_bases_init_path = Path('bases').joinpath('__init__.py')
    spec = util.spec_from_file_location('bases', t_bases_init_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
except FileNotFoundError:
    raise('bases/__init__.py not found in root directory. Please run "python app.py prepare" in application root directory.')