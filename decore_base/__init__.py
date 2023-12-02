from .globals import globals
from .decore import decore

if globals.flags.production_mode or globals.flags.dev_mode:
    from .bases import *