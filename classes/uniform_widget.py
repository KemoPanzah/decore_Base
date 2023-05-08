from .uniform_object import Uniform_object
from .uniform_list import Uniform_list

class Uniform_widget(Uniform_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc, p_type, p_layout, p_active_s):
        Uniform_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.type = p_type
        self.layout = p_layout
        self.active_s = Uniform_list(p_active_s)