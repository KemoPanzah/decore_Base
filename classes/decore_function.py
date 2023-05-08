from .decore_object import Decore_object

class Decore_function(Decore_object):
     def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc, p_type, p_func):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.type = p_type
        self.func = p_func