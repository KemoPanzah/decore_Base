from .decore_object import Decore_object
from .decore_list import Decore_list

class Decore_widget(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc, p_type, p_layout, p_active_s):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.type = p_type
        self.layout = p_layout
        self.active_s = Decore_list(p_active_s)