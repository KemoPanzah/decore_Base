from .uniform_object import Uniform_object
from .uniform_list import Uniform_list


class Uniform_dialog(Uniform_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc, p_type, p_display, p_activator):
        Uniform_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.type = p_type
        self.display = p_display
        self.activator = p_activator
