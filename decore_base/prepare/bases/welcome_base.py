from decore_base import decore
from models.welcome_model import Welcome_model

@decore.base(title='Welcome', icon='mdi-home', model=Welcome_model)
class Welcome_base:
   pass