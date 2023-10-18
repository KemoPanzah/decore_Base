from .decore_object import Decore_object

class Decore_app(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_allow_guest):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc)
        self.allow_guest = p_allow_guest
        self.base_id = None
        self.view_id = None