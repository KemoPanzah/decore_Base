class Decore_object(object):
    def __init__(self, p_kind, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_role):
        self.kind = p_kind
        self.parent_kind = None
        self.id = p_id
        self.parent_id = p_parent_id
        self.source_id = p_source_id
        self.icon = p_icon
        self.title = p_title
        self.desc = p_desc
        self.role = p_role
        # self.base_id_s = []
        # self.view_id_s = []
        # self.dialog_id_s = []
        # self.widget_id_s = []
        # self.action_id_s = []
        # self.element_id_s = []
        self.base_s = []
        self.view_s = []
        self.dialog_s = []
        self.widget_s = []
        self.action_s = []
        self.element_s = []