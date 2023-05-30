from ...classes import Decore_base, Decore_model
from ...library import Particl_market

from datetime import datetime
import json

#TODO - rename | Market_object_extender
class Particl_market_objects(object):
    def __init__(self, p_particl_market:Particl_market):
        t_time = datetime.now()
        self.particl_market = p_particl_market
        self.template_s = self.particl_market.template_search(0, 999999, 'ASC', 'updated_at')
        self.bid_s = self.particl_market.bid_search(0, 999999, 'ASC', 'updated_at')

        self.extend_template_s()
        print ('[INFO] Mox needs ' + str((datetime.now() - t_time).total_seconds()) + ' seconds for call')

    def extend_template_s(self):     
        for i_template in self.template_s:
            self.extend_template_listings(i_template)
        
        for i_template in self.template_s:
            self.extend_template(i_template)

    #TODO - rename | extend_template_listingitems_bids
    def extend_template_listings(self, p_template):
        #TODO - index wird nicht mehr benötigt
        for index, i_listing_item in enumerate(p_template['ListingItems']):
            i_listing_item['Bids'] = []
            for i_bid in self.bid_s:
                if i_listing_item['id'] == i_bid['listingItemId']:
                    i_listing_item['Bids'].append(i_bid)
    
    def extend_template(self, p_template):    
        for index, i_child_template in enumerate(p_template['ChildListingItemTemplates']):
            p_template['ChildListingItemTemplates'][index] = self.get_template(i_child_template['id'])
            self.extend_template(p_template['ChildListingItemTemplates'][index])

    def get_base_template_s(self):
        r_value = []
        for i_template in self.template_s:
            if not i_template['parentListingItemTemplateId']:
                r_value.append(i_template)
        return r_value

    def get_template(self, p_template_id):
        r_value = None
        for i_template in self.template_s:
            if p_template_id == i_template['id']:
                r_value = i_template
        return r_value

class Askform_model(Decore_model):
    def __init__(self, p_particl_market=None):
        self.particl_market = p_particl_market
        self.template:dict = None
        self.template_id = None
        self._focus = None
        Decore_model.__init__(self)
    
    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, p_value):
        t_title = json.loads(self.template['ItemInformation']['title'])
        t_summary = self.template['ItemInformation']['shortDescription']
        t_data = self.template['ItemInformation']['longDescription']
        t_category_id = self.template['ItemInformation']['itemCategoryId']
        t_title['focus'] = p_value
        if self.particl_market.information_update(self.template_id, json.dumps(t_title), t_summary, t_data, t_category_id):
            self._focus = p_value

    @property
    def active_child_template_s(self):
        return self.__get_active_child_templates_s(self.template)
    
    @property
    def orderitem_s(self):
        r_value = []
        for i_template in self.__get_child_templates_s(self.template):
            for i_listingitem in i_template['ListingItems']:
                for i_bid in i_listingitem['Bids']:
                    if i_bid['OrderItem']: 
                        r_value.append(i_bid['OrderItem'])
        return r_value

    @property
    def root_bid_s(self):
        r_value = []
        for i_template in self.__get_child_templates_s(self.template):
            for i_listingitem in i_template['ListingItems']:
                for i_bid in i_listingitem['Bids']:
                    if i_bid['OrderItem']: 
                        r_value.append(i_bid)
        return r_value
    
    def __get_child_templates_s(self, p_template, p_days_rent=1):
        r_value=[]
        if p_template['parentListingItemTemplateId']:
            r_value.append(p_template)
        for i_child_template in p_template['ChildListingItemTemplates']:
            r_value = r_value + self.__get_child_templates_s(i_child_template)
        return r_value

    def __get_active_child_templates_s(self, p_template, p_days_rent=1):
        r_value=[]
        if p_template['parentListingItemTemplateId']:
            t_ts_now = int(datetime.timestamp(datetime.now()))*1000
            t_ts_rent = 86400000 * p_days_rent
            t_ts_float = t_ts_now - int(p_template['updatedAt'])
            if p_template['hash'] and t_ts_float < t_ts_rent: r_value.append(p_template)
        for i_child_template in p_template['ChildListingItemTemplates']:
            r_value = r_value + self.__get_active_child_templates_s(i_child_template)
        return r_value
    
    def get_shipping_memo_by_root_bid(self, p_bid):
        for i_child_bid in p_bid['ChildBids']:
            if i_child_bid['type'] == 'MPA_SHIP':
                for i_biddata in i_child_bid['BidDatas']:
                    if i_biddata['key'] == 'shipping.memo':
                        return i_biddata

    def publish(self, p_price, p_days_rent=1):
        #Sammle Informationen von BaseTemplate
        t_title = self.template['ItemInformation']['title']
        t_summary = self.template['ItemInformation']['shortDescription']
        t_data = self.template['ItemInformation']['longDescription']
        t_category_id = self.template['ItemInformation']['itemCategoryId']
        
        #Bereinige nicht genutzes ChildTemplate
        for i_child_template in self.template['ChildListingItemTemplates']:
            if not i_child_template['hash']:
                self.particl_market.template_remove(i_child_template['id'])

        #Erstelle ein Duplikat
        t_clone = self.particl_market.template_clone(self.template['id'])
        
        if t_clone:
            #Vervollständige Informationen des Duktikates und poste das an den Markt
            self.particl_market.information_update(t_clone['id'], t_title, t_summary, t_data, t_category_id)
            self.particl_market.payment_update(t_clone['id'], 'SALE', 'PART', p_price, 0, 0)
            self.particl_market.location_update(t_clone['id'])
            t_post = self.particl_market.template_post(t_clone['id'], p_days_rent)
            
            if t_post:
                return True
            else:
                self.particl_market.template_remove(t_clone['id'])
                return False
        else:
            return False

#TODO - das ist eigentlich die Bidform_base | Alter wieder alles umbenennen!
class Askform_base(Decore_base):
    def __init__(self, model):
        self.particl_market = Particl_market()
        self._version_s = ['fhan']
        Decore_base.__init__(self, model)
  
    def add_item(self, p_item):
        r_value = p_item.validate()
        if r_value == True:
            t_title = {'id': p_item.id, 'scope': self.scope, 'focus': '*', 'version': self._version_s[-1]}
            self.particl_market.template_add(json.dumps(t_title), 'null', json.dumps(p_item.__data__), 76, "SALE", "PART", 1, 0, 0)
        return r_value

    def get_all(self):
        t_item_s = []		
        t_pmo = Particl_market_objects(self.particl_market)
        t_market_item_s = t_pmo.get_base_template_s()
        if t_market_item_s:
            for t_market_item in t_market_item_s:
                try:
                    t_title = json.loads(t_market_item['ItemInformation']['title'])
                except Exception as error:
                    continue                   
                else:
                    if ('scope' in t_title and 'version' in t_title) and (t_title['scope'] == self.scope and t_title['version'] in self._version_s):
                        t_data = json.loads(t_market_item['ItemInformation']['longDescription'])
                        t_item = self.model(self.particl_market)
                        t_item.__data__.update(t_data)
                        t_item.template = t_market_item
                        t_item.template_id = t_market_item['id']
                        t_item._focus = t_title['focus']
                        t_item_s.append(t_item)
                    else:
                        self.particl_market.information_update(t_market_item['id'], 'remove', 'null', 'null', 76)
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