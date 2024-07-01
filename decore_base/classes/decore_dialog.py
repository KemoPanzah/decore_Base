from .decore_object import Decore_object
from .decore_list import Decore_list

class Decore_dialog(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_hide, p_role, p_type, p_activator):
        Decore_object.__init__(self, 'dialog', p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_hide, p_role)
        self.type = p_type
        self.activator = p_activator
