from ...classes import Decore_base, Decore_model
from ...library import Particl_market

from datetime import datetime
import json

class Market_object_extender(object):
    def __init__(self, p_particl_market:Particl_market):
        t_time = datetime.now()
        self.particl_market = p_particl_market
        self.item_s = self.particl_market.item_search(0, 999999, 'ASC', 'updated_at')
        self.comment_s = self.particl_market.comment_search(0, 999999, 'ASC', 'updated_at', 'LISTINGITEM_QUESTION_AND_ANSWERS')

        self.extend_item_s()
        print ('[INFO] Mox needs ' + str((datetime.now() - t_time).total_seconds()) + ' seconds for call')

    def extend_item_s(self):     
        for i_item in self.item_s:
            self.extend_item_comments(i_item)
        
    def extend_item_comments(self, p_item):
        p_item['Comments'] = []
        for i_comment in self.comment_s:
            if p_item['hash'] == i_comment['target'] and p_item['seller'] == i_comment['sender']:
                p_item['Comments'].append(i_comment)
    
    def get_item_s(self):
        r_value = []
        for i_item in self.item_s:
            r_value.append(i_item)
        return r_value
    
class Buyform_model(Decore_model):
    def __init__(self):
        self.listingitem:dict = None
        self.listingitem_id = None
        Decore_model.__init__(self)
        
class Buyform_base(Decore_base):
    def __init__(self, model):
        self.particl_market = Particl_market()
        self._version_s = ['fhan']
        Decore_base.__init__(self, model)

    def get_all(self, p_mode = 'all'):
        t_item_s = []
        t_mox = Market_object_extender(self.particl_market)
        t_market_item_s = t_mox.get_item_s()
        if t_market_item_s:
            for t_market_item in t_market_item_s:
                try:
                    t_title = json.loads(t_market_item['ItemInformation']['title'])
                except Exception as error:
                    continue
                else:
                    if ('scope' in t_title and 'version' in t_title) and (t_title['scope'] == self.scope and t_title['version'] in self._version_s):
                        t_data = json.loads(t_market_item['ItemInformation']['longDescription'])
                        t_item = self.model()
                        t_item.__data__.update(t_data)
                        t_item.listingitem = t_market_item
                        t_item.listingitem_id = t_market_item['id']

                        t_comment_s = t_market_item['Comments']
                        
                        if p_mode == 'all':
                             t_item_s.append(t_item)

                        if p_mode == 'public':   
                            if t_title['focus'] == '*':
                                if not t_comment_s or (t_comment_s and t_comment_s[-1]['message'] == 'AWAITING_ESCROW'):
                                    t_item_s.append(t_item)
                            
                        if p_mode == 'private': 
                            if t_title['focus'] == self.particl_market.get_identity_address():
                                t_item_s.append(t_item)
            
        return self.normalize_item_s(t_item_s)

    def normalize_item_s(self, p_item_s):
        t_item_s = []
        for i_item in p_item_s:
            t_found_id = False
            for i_temp_item in t_item_s:
                if i_temp_item.id == i_item.id:
                    t_found_id = True
                    break
            if t_found_id == True:
                continue
            t_item = None
            t_market_item_created_at = 0

            for i_check_item in p_item_s:
                if i_check_item.id == i_item.id and i_check_item.listingitem['createdAt'] > t_market_item_created_at:
                    t_item = i_check_item
                    t_market_item_created_at = i_check_item.listingitem['createdAt']
            t_item_s.append(t_item)
        return t_item_s

    def get_dicts(self):
        t_dicts = []
        for i_item in self.get_all('public'):
            t_dicts.append(i_item.__data__)
        return t_dicts

    def get_by_id(self, id):
        r_value = None
        for i_item in self.get_all():
            if i_item.id == id:
                r_value = i_item
                break
        return r_value

    ####################################################################################################################################################