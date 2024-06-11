from .decore_object import Decore_object

class Decore_app(Decore_object):
    def __init__(self, p_title, p_desc, p_role):
        Decore_object.__init__(self,'app', 'app', 'root', None, None, p_title, p_desc, False, p_role)