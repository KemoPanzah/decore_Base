from .decore_object import Decore_object

class Decore_app(Decore_object):
    def __init__(self, p_title, p_desc, p_role, p_allow_guest):
        Decore_object.__init__(self,'app', 'app', 'root', None, None, p_title, p_desc, p_role)
        self.allow_guest = p_allow_guest