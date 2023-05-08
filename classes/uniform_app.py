from .uniform_object import Uniform_object

class Uniform_app(Uniform_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc):
        Uniform_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.base_id = None
        self.view_id = None