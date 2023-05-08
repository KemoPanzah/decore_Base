from .decore_object import Decore_object

class Decore_view(Decore_object):
    def __init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title,p_desc, p_doc, p_type, p_active_s, p_filter_s, p_query, p_pag_type, p_pag_recs):
        Decore_object.__init__(self, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_doc)
        self.type = p_type
        self.active_s = p_active_s
        self.filter_s = p_filter_s
        self.query = p_query
        self.pag_type = p_pag_type
        self.pag_recs = p_pag_recs