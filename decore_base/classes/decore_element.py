from .decore_object import Decore_object
from .decore_list import Decore_list

class Decore_element(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_type, p_default, p_disable, p_schema, p_func):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc)
        self.type = p_type
        self.default = p_default
        self.disable = p_disable
        self.schema = p_schema
        self.func = p_func