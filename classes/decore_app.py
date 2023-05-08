from .decore_object import Decore_object

class Decore_app(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.base_id = None
        self.view_id = None