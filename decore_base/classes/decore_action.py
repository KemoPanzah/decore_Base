from .decore_object import Decore_object


class Decore_action(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_role, p_type, p_activator, p_errors, p_func):
        Decore_object.__init__(self, 'action', p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_role)
        self.type = p_type
        self.activator = p_activator
        self.errors = p_errors
        self.func = p_func
