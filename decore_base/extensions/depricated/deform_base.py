from ...classes import Decore_base, Decore_model

from pysyncobj import SyncObj, SyncObjConf, replicated
from pathlib import Path

class Deform_base(Decore_base, SyncObj):
    def __init__(self, scope, caption, model):
        Decore_base.__init__(self, scope, caption, model)
        SyncObj.__init__(self,self.get_server_address(), self.get_node_address_s(), self.get_sync_config())
        self.item_s = []

    def get_server_address(self):
        r_value = '127.0.0.1:' + self.config.get('NETWORK','raft_port')
        return r_value

    def get_node_address_s(self):
        r_value = []
        for i_node in str(self.config.get('NETWORK','raft_nodes')).split():
            r_value.append(i_node)
        return r_value
    
    def get_sync_config(self):
        r_value = SyncObjConf(fullDumpFile=Path(self.state_path).joinpath(self.scope + '.bin'))
        return r_value

    @replicated
    def add_item(self, p_item: Decore_model):
        r_value = p_item.validate()
        if r_value == True:
            self.item_s.append(p_item)
        return r_value

    def delete_by_id(self, id):
        t_index = None
        for i, i_item in enumerate(self.item_s):
            if i_item.id == id:
                t_index = i
                break
        if t_index != None:
            self.item_s.pop(t_index)

    def get_all(self):
        t_item_s = self.item_s
        return (t_item_s)

    def get_dicts(self):
        t_dict_s = []
        for i_item in self.item_s:
            t_dict_s.append(i_item.__data__)
        return t_dict_s

    def get_by_id(self, id):
        r_value = None
        for i_item in self.item_s:
            if i_item.id == id:
                r_value = i_item
                break
        return r_value