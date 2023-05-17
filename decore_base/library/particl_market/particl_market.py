import json
import requests

class Return_values(object):
    def __init__(self, p_value):
        self.result = None
        self.error = None
        self.set_values(p_value)

    def set_values(self, p_value):
        if type(p_value) == str and '[ERROR]' in p_value:
            self.result = None
            self.error = p_value
            print (self.error)
        else:
            self.result = p_value
            self.error = None

class Particl_market(object):
    def __init__(self, port=45492, profile_id=1, country='DE', market_key='7wASZuVnRd4TePTDsTD9Dgtj6Vk5fCFL5nnznFcEBVc3wyeRm3xq'):
        self.port = port
        self.profile_id = profile_id
        self.country = country
        self.market_key = market_key

    def json_request(self, method:str, *params:str):
        r_value = None
        try:
            t_url = 'http://127.0.0.1:' + str(self.port) + '/api/rpc'
            t_params:list = []
            for i_param in params: t_params.append(i_param)
            t_data = json.dumps({"jsonrpc":"2.0", "method":method, "params":t_params})
            t_headers = {'content-type': "application/json", 'cache-control': "no-cache"}
            response = requests.request("POST", t_url, data=t_data, headers=t_headers)
            r_value =  json.loads(response.text)
        except Exception as error:
            return Return_values('json_request [ERROR] >> ' + str(error))
        else:
            if 'error' in r_value:
                return Return_values('json_request [ERROR] >> ' + str(r_value['error']))
            else:
                return Return_values(r_value['result'])


    def get_identity_address(self, p_type='MARKET'):
        t_value = self.identity_list()
        if t_value:
            for i_identity in t_value:
                if i_identity['type'] == p_type:
                    return i_identity['address']

    def get_identity_id(self, p_type='MARKET'):
        t_value = self.identity_list()
        if t_value:
            for i_identity in t_value:
                if i_identity['type'] == p_type:
                    return i_identity['id']
    
    def get_market_id(self, p_market_key):
        t_value = self.market_list()
        if t_value:
            for i_market in t_value:
                if i_market['receiveKey'] == p_market_key:
                    return i_market['id']
    
    def get_market_address(self, p_market_key):
        t_value = self.market_list()
        if t_value:
            for i_market in t_value:
                if i_market['receiveKey'] == p_market_key:
                    return i_market['receiveAddress']

#####################################################################################################################################################

    def template_post(self, template_id, days_retanation, estaminate_fee=False):
        t_request = self.json_request('template', 'post', template_id, days_retanation, estaminate_fee)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def template_search(self, page, page_limit, order, order_field):
        t_request = self.json_request('template', 'search', page, page_limit, order, order_field, self.profile_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return []

    def template_get(self, template_id):
        t_request = self.json_request('template', 'get', template_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def template_add(self, title, short_description, long_description, category_id, payment_type, currency, base_price, d_shipping_price, i_shipping_price):
        t_request = self.json_request('template', 'add', self.profile_id, title, short_description, long_description, category_id, payment_type, currency, base_price, d_shipping_price, i_shipping_price)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def template_clone(self, template_id):
        t_request = self.json_request('template', 'clone', template_id, self.get_market_id(self.market_key))
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None
    
    def template_remove(self, template_id):
        t_request = self.json_request('template', 'remove', template_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def information_update(self, template_id, title, short_description, long_description, category_id):
        t_request = self.json_request('information', 'update', template_id, title, short_description, long_description, category_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def location_update(self, template_id):
        t_request = self.json_request('location', 'update', template_id, self.country)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def identity_list(self):
        t_request = self.json_request('identity', 'list', self.profile_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def market_list(self):
        t_request = self.json_request('market', 'list', self.profile_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def item_search(self, page, page_limit, order, order_field):
        t_request =  self.json_request('item', 'search', page, page_limit, order, order_field, self.get_market_address(self.market_key))
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return []

    def item_get(self, id):
        t_request = self.json_request('item', 'get', id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def bid_send(self, listingitem_id):
        t_request = self.json_request('bid', 'send', listingitem_id, self.get_identity_id(), 1)
        if not t_request.error: 
            return t_request.result
        else: 
            breakpoint()
            return None

    def bid_accept(self, bid_id):
        t_request = self.json_request('bid', 'accept', bid_id, self.get_identity_id())
        if not t_request.error: 
            return t_request.result
        else: 
            breakpoint()
            return None
    
    def bid_cancel(self, bid_id):
        t_request = self.json_request('bid', 'cancel', bid_id, self.get_identity_id())
        if not t_request.error: 
            return t_request.result
        else: 
            breakpoint()
            return None

    def bid_reject(self, bid_id, reason):
        t_request = self.json_request('bid', 'reject', bid_id, self.get_identity_id(), reason)
        if not t_request.error: 
            return t_request.result
        else: 
            breakpoint()
            return None

    def bid_search(self, page, page_limit, order, order_field):
        t_request = self.json_request('bid', 'search', page, page_limit, order, order_field, self.profile_id)
        if not t_request.error: 
            return t_request.result
        else: 
            breakpoint()
            return None

    def payment_update(self, template_id, payment_type, currency, base_price, d_shipping_price, i_shipping_price):
        t_request = self.json_request('payment', 'update', template_id, payment_type, currency, base_price, d_shipping_price, i_shipping_price)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None
    
    def currencyprice(self, currency):
        t_request = self.json_request('currencyprice', 'PART', currency)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint() 
            return None

    def cartitem_add(self, listingitem_id):
        t_request = self.json_request('cartitem', 'add', 1, listingitem_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def cartitem_list(self):
        t_request = self.json_request('cartitem', 'list', 1)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint() 
            return None

    def escrow_lock(self, orderitem_id):
        t_request = self.json_request('escrow', 'lock', orderitem_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None
    
    def escrow_complete(self, orderitem_id):
        t_request = self.json_request('escrow', 'complete', orderitem_id)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint() 
            return None

    def orderitem_ship(self, orderitem_id, memo):
        t_request = self.json_request('orderitem', 'ship', orderitem_id, memo)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None

    def comment_post(self, p_type, p_target, p_message):
        t_request:Return_values = self.json_request('comment', 'post', self.get_identity_id(), p_type, self.get_market_address(self.market_key), p_target, p_message)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return None
    #TODO - Alle Paramter die durch Funktionen ermittelt werden ersetzen und ermmituung in der jeweiligen Base-Klasse
    def comment_search(self, page, page_limit, order, order_field, ctype, target=None, sender=None):
        t_request = self.json_request('comment', 'search', page, page_limit, order, order_field, ctype, self.get_market_address(self.market_key), target, sender)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return []

    def order_search(self, page, page_limit, order, order_field):
        t_request = self.json_request('order', 'search', page, page_limit, order, order_field)
        if not t_request.error: 
            return t_request.result
        else:
            breakpoint()
            return []