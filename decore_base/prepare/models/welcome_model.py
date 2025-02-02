from decore_base.uniform.conform_model import *

class Welcome_model(Conform_model):
   firstname = CharField(verbose_name='First Name')
   lastname = CharField(verbose_name='Last Name')