from ...classes import Decore_base, Decore_model
from ...library import Particl_market

from pathlib import Path
from datetime import datetime
import json

class Conform_base(Decore_base, Particl_market):
    def __init__(self, scope, caption, model, mode):
        Decore_base.__init__(self, scope, caption, model)
        Particl_market.__init__(self)
        self.mode = mode
        
    def add_item(self, p_item: Decore_model):
        r_value = p_item.validate()
        if r_value == True:
            t_title = {'id': p_item.id, 'scope': self.scope}
            self.add_template(json.dumps(t_title), 'null', json.dumps(p_item.__data__), 76, "SALE", "PART", 1, 0, 0)
        return r_value

    def get_all(self):
        t_item_s = []
        
        if self.mode == 'SELLER': t_market_item_s = self.get_base_template_list()
        if self.mode == 'BIDDER': t_market_item_s = self.get_item_list()

        if t_market_item_s:

            for t_market_item in t_market_item_s:
                try:
                    t_title = json.loads(t_market_item['ItemInformation']['title'])
                except Exception as error:
                    continue
                else:
                    if 'scope' in t_title and t_title['scope'] == self.scope:
                        t_data = json.loads(t_market_item['ItemInformation']['longDescription'])
                        t_item = type(self.model)()
                        for i_key, i_value in t_data.items():
                            setattr(t_item, i_key, i_value)
                        #TODO - umbenennen market_item_dict in pmi_dict > der Rest (id, created_at können entfernt werden) wird aus dem dict ausgelesen.
                        setattr(t_item, 'market_item_id', t_market_item['id'])
                        setattr(t_item, 'market_item_created_at', t_market_item['createdAt'])
                        setattr(t_item, 'market_item_dict', t_market_item)
                        t_item_s.append(t_item)
        
        if self.mode == 'SELLER': return t_item_s
        if self.mode == 'BIDDER': return self.normalize_item_s(t_item_s)

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
                if i_check_item.id == i_item.id and i_check_item.market_item_created_at > t_market_item_created_at:
                    t_item = i_check_item
                    t_market_item_created_at = i_check_item.market_item_created_at
            
            #for i_bid in t_item.market_item_dict['Bids']:
            #	if i_bid['OrderItem'] and i_bid['OrderItem']['status'] == 'BIDDED':
            #		t_bidded = True
            
            t_summary = json.loads(t_item.market_item_dict['ItemInformation']['shortDescription'])
            if t_summary['bidder'] == '*' or t_summary['bidder'] == self.get_identity_address():
                t_item_s.append(t_item)
        return t_item_s

    def get_dicts(self):
        t_dicts = []
        for i_item in self.get_all():
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

    def add_template(self, title, short_description, long_description, category_id, sale_type, currency, base_price, d_shipping_price, i_shipping_price):
        t_result = self.template_add(title, short_description, long_description, category_id, sale_type, currency, base_price, d_shipping_price, i_shipping_price)
        if not t_result.error and not 'error' in t_result.result:
            return True
        else:
            return False
    
    #Todo - p_day_rent=1 anstatt days_rentanation
    def post_template(self, p_base_template_id, p_market_address, p_price, p_days_rent, p_bidder='*'):
        # Holen des Template dicts
        t_template = self.get_template(p_base_template_id)

        #Todo prüfe auf base_template in einer extra Funktion

        #Sammle Informationen von BaseTemplate
        t_title = t_template['ItemInformation']['title']
        t_data = t_template['ItemInformation']['longDescription']
        t_category_id = t_template['ItemInformation']['itemCategoryId']
        
        #Bereinige nicht genutzes ChildTemplate
        for i_child_template in t_template['ChildListingItemTemplates']:
            if i_child_template['market'] == self.get_market_address():
                if not i_child_template['hash']:
                    self.template_remove(i_child_template['id'])

        #Erstelle ein Duplikat
        t_result1 = self.template_clone(p_base_template_id, self.get_market_id())
        
        if not t_result1.error and not 'error' in t_result1.result:
            #Vervollständige Informationen des Duktikates und poste das an den Markt
            t_summary = {'days_rent': p_days_rent, 'bidder': p_bidder}
            #Todo - wrappen der folgenden funktionen in particle_market
            self.information_update(t_result1.result['result']['id'], t_title, json.dumps(t_summary), t_data, t_category_id)
            self.payment_update(t_result1.result['result']['id'], 'SALE', 'PART', p_price, 0, 0)
            self.location_update(t_result1.result['result']['id'])
            t_result2 = self.template_post(t_result1.result['result']['id'], p_days_rent)
            
            if not t_result2.error and not 'error' in t_result2.result:
                return True
            else:
                self.template_remove(t_result1.result['result']['id'])
                return False
        else:
            return False
    
    def get_template_listing_s(self, p_template, p_market_address, p_days_rent=1):
        r_value=[]
        if p_template['parentListingItemTemplateId'] and p_template['market'] == p_market_address:
            t_ts_now = int(datetime.timestamp(datetime.now()))*1000
            t_ts_rent = 86400000 * p_days_rent
            t_ts_float = t_ts_now - int(p_template['updatedAt'])
            if p_template['hash'] and t_ts_float < t_ts_rent: r_value.append(p_template)
        if 'ChildListingItemTemplates' in p_template:
            for i_child_template in p_template['ChildListingItemTemplates']:
                r_value = r_value + self.get_template_listing_s(i_child_template, p_market_address)
        return r_value

    def get_template_listing_count(self, p_template, p_market_address, p_days_rent=1):
        r_value=0
        if p_template['parentListingItemTemplateId'] and p_template['market'] == p_market_address:
            t_ts_now = int(datetime.timestamp(datetime.now()))*1000
            t_ts_rent = 86400000 * p_days_rent
            t_ts_float = t_ts_now - int(p_template['updatedAt'])
            if p_template['hash'] and t_ts_float < t_ts_rent: r_value += 1
        if 'ChildListingItemTemplates' in p_template:
            for i_child_template in p_template['ChildListingItemTemplates']:
                r_value = r_value + self.get_template_listing_count(i_child_template, p_market_address)
        return r_value