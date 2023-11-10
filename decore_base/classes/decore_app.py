from .decore_object import Decore_object

class Decore_app(Decore_object):
    def __init__(self, p_title, p_desc, p_allow_guest):
        Decore_object.__init__(self,'app', 'app', None, None, None, p_title, p_desc, 0)
        self.allow_guest = p_allow_guest
        # self.start_base_id = None
        # self.view_id = None