class Decore_list(list):
    def __init__(self, p_i_s=[]):
        list.__init__(self)
        for i in p_i_s:
            self.append(i)
    #OUT - Kann nach übernahme der Decore_pools entfernt werden
    def get_by_id(self, p_id):
        for i in self:
            if i.id == p_id:
                return i
    #OUT - Kann nach übernahme der Decore_pools entfernt werden
    def get_s_by_parent_id(self, p_parent_id):
        r_s = Decore_list()
        for i in self:
            if i.parent_id == p_parent_id:
                r_s.append(i)
        return r_s

    #OUT - Kann nach übernahme der Decore_pools entfernt werden
    def export(self):
        r_value = []
        for i in self:
            t_dict = dict()
            for key, value in i.__dict__.items():
                if type(value) is type(self):
                    t_dict[key] = value.export()
                elif type(value) is dict or type(value) is str or type(value) is bool or type(value) is int:
                    t_dict[key] = value
                # elif type(value) is Decore_translate:
                #     t_dict[key] = value.output
                elif key == 'choices':
                    t_dict[key] = []
                elif not value:
                    t_dict[key] = None
                else:
                    t_dict[key] = str(value)
            t_dict['class'] = str(i)
            r_value.append(t_dict)
        return r_value
