from .decore_object import Decore_object

class Decore_template(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_hide, p_role, p_func):
        Decore_object.__init__(self, 'template', p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_hide, p_role)
        self.func = p_func