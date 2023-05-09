from .classes.decore_action import Decore_action
from .classes.decore_app import Decore_app
from .classes.decore_base import Decore_base
from .classes.decore_dialog import Decore_dialog
from .classes.decore_element import Decore_element
from .classes.decore_function import Decore_function
from .classes.decore_model import Decore_model
from .classes.decore_pool import Decore_pool
from .classes.decore_query import Decore_query
from .classes.decore_view import Decore_view
from .classes.decore_widget import Decore_widget
from .classes.decore_prompt import Decore_prompt

from . import globals

from playhouse.shortcuts import model_to_dict
from uuid import uuid1
from typing import Literal
from time import perf_counter

from flask import Flask, render_template, request, jsonify, send_file
from flask_wtf.csrf import generate_csrf
from flask_cors import CORS

import json, logging
from str2type import str2type
from pathlib import Path
from collections import OrderedDict


class Decore(object):
    def __init__(self):
        self.prompt = Decore_prompt()
        self.pool = Decore_pool()
        self.api = self.get_api()
        Decore_query.create_table(safe=True)
        
    def get_api(self):
        t_static_folder = Path('spa/static')
        t_template_folder = Path('spa/templates')
        api = Flask(__name__, static_folder=t_static_folder.absolute(), template_folder=t_template_folder.absolute())
        CORS(api, expose_headers=["Content-Disposition"])
        # Make the WSGI interface available at the top level so wfastcgi can get it.
        wsgi_app = api.wsgi_app
        api.config['SECRET_KEY'] = '325245hkhf486axcv5719bf9397cbn69xv'
        api.config['WTF_CSRF_ENABLED'] = False  # TODO - csrf enebled when not cors
        print('APP_ROOT_FOLDER >> ' + str(api.root_path))
        print('STATIC_FOLDER >> ' + str(api.static_folder))
        print('TEMPLATE_FOLDER >> ' + str(api.template_folder))
        api.add_url_rule('/', 'index', self.index, defaults={'p_path': ''})
        api.add_url_rule('/<path:p_path>', 'index', self.index)
        api.add_url_rule('/get_meta', 'get_meta', self.get_meta)
        api.add_url_rule('/get_default/<p_source_id>', 'get_default', self.get_default)
        api.add_url_rule('/get_last/<p_source_id>', 'get_last', self.get_last)
        api.add_url_rule('/post_item_s/<p_source_id>', 'post_item_s', self.post_item_s, methods=['POST'])
        api.add_url_rule('/post_option_s/<p_source_id>', 'post_option_s', self.post_option_s, methods=['POST'])
        api.add_url_rule('/post_action/<p_action_id>', 'post_action', self.post_action, methods=['POST'])
        api.add_url_rule('/get_query_s', 'get_query_s', self.get_query_s)
        api.add_url_rule('/post_save_query/<p_base_id>/<p_view_id>', 'post_save_query', self.post_save_query, methods=['POST'])
        api.add_url_rule('/get_remove_query/<p_id>', 'get_remove_query', self.get_remove_query)
        return api

    def start_api(self):
        import os, sys
        from waitress import serve
        HOST = os.environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(os.environ.get('SERVER_PORT', str(globals.config.app_port)))
        except ValueError:
            PORT = globals.config.app_port
        
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            serve(self.api, host=HOST, port=PORT)
        else:
            self.api.run(HOST, PORT)

    def app(self, p_title):
        def wrapper(func):
            self.pool.register(Decore_app('app', None, None, None, p_title, None, func.__doc__))
            self.pool.extend()
            for i_base in self.pool.base_s:
                i_base.start_inits()
                i_base.start_worker()
            self.start_api()
        return wrapper

    def base(self, p_icon=None, p_title=None, p_desc=None, p_model=Decore_model):
        def wrapper(cls):
            t_base: Decore_base = cls()
            t_base.id = cls.__name__
            t_base.icon = p_icon
            t_base.title = p_title
            t_base.desc = p_desc
            t_base.doc = cls.__doc__
            t_base.model = p_model.register()
            t_base.field_s = p_model.field_s
            t_base.rel_field_s = p_model.rel_field_s
            t_base.schema = p_model.build_schema()
            self.pool.register(t_base)
        return wrapper

    l_view_type = Literal['table']
    l_view_pag_type = Literal['client']

    def view(self, p_parent_id=None, p_icon=None, p_title=None, p_desc=None, p_type: l_view_type = 'table', p_active_s=[], p_filter_s=[], p_query={}, p_pag_type: l_view_pag_type = 'client', p_pag_recs=16):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not p_parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = p_parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_view(func.__name__, t_parent_id, t_source_id, p_icon, p_title, p_desc, func.__doc__, p_type, p_active_s, p_filter_s, p_query, p_pag_type, p_pag_recs))
            func()
        return wrapper

    l_dialog_type = Literal['standard', 'tabs', 'stepper']
    l_dialog_display = Literal['modal', 'drawer']
    l_dialog_activator = Literal['none', 'default-menu', 'item-menu', 'item-click']

    # TODO - Überprüfen ob element mit gleicher ID schon vorhanden ist und Execption
    def dialog(self, p_parent_id=None, p_icon=None, p_title=None, p_desc=None, p_type: l_dialog_type = 'standard', p_display: l_dialog_display = 'drawer', p_activator: l_dialog_activator = 'none'):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not p_parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = p_parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_dialog(func.__name__, t_parent_id, t_source_id, p_icon, p_title, p_desc, func.__doc__, p_type, p_display, p_activator))
            func()
        return wrapper

    l_widget_type = Literal['default', 'info', 'form', 'table']

    def widget(self, p_parent_id=None, p_icon=None, p_title=None, p_desc=None, p_type: l_widget_type = 'default', p_layout='cera', p_active_s=[]):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not p_parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = p_parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_widget(func.__name__, t_parent_id, t_source_id, p_icon, p_title, p_desc, func.__doc__, p_type, p_layout, p_active_s))
            func()
        return wrapper

    l_element_type = Literal['p', 'checkbox']

    def element(self, p_parent_id=None, p_icon=None, p_title=None, p_desc=None, p_type: l_element_type = 'text', p_default=None, p_disable=False, p_schema=None):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not p_parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = p_parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_element(func.__name__, t_parent_id, t_source_id, p_icon, p_title, p_desc, p_type, p_default, p_disable, p_schema, func))
        return wrapper

    l_action_type = Literal['standard', 'check', 'response', 'file'] #TODO - check, response > activators
    l_action_activator = Literal['none', 'default-menu', 'item-submit', 'item-menu', 'item-click']

    def action(self, p_parent_id=None, p_icon=None, p_title=None, p_desc=None, p_type: l_action_type = 'standard', p_activator: l_action_activator = 'none'):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not p_parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = p_parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_action(func.__name__, t_parent_id, t_source_id, p_icon, p_title, p_desc, func.__doc__, p_type, p_activator, func))
        return wrapper

    l_function_type = Literal['init', 'worker']
  
    def function(self, p_type:l_function_type = 'init'):
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            t_parent_id = t_parent_s[-2]
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_function(func.__name__, t_parent_id, t_source_id, None, None, None, func.__doc__, p_type, func))
        return wrapper

    def get_base_by_id(self, p_id):
        i_base: Decore_base
        for i_base in self.pool.base_s:
            if i_base.id == p_id:
                return i_base

    def get_base_by_model(self, p_model) -> Decore_base:
        i_base: Decore_base
        for i_base in self.pool.base_s:
            if i_base.model == p_model:
                return i_base

    def get_base_by_module(self, p_module):
        i_base: Decore_base
        for i_base in self.pool.base_s:
            if i_base.__module__ == p_module:
                return i_base
    
    #### Api methods ####

    def index(self, p_path):
        return render_template('index.html', port=globals.config.app_port)
    
    def get_meta(self):
        return jsonify(self.pool.export())
    
    def get_default(self, p_source_id):
        t_source = self.pool.__data__[p_source_id]
        t_item = t_source.model().__data__
        return jsonify(t_item), 200
    
    def get_last(self, p_source_id):
        t_source = self.pool.__data__[p_source_id]
        t_item = t_source.model.select()[0].__data__
        return jsonify(t_item), 200

    def post_item_s(self, p_source_id):
        t_start = perf_counter()
        t_query = json.loads(request.data)
        t_source = self.pool.__data__[p_source_id]
        t_item_s = t_source.model.get_dict_s(t_query)
        t_end = perf_counter()
        logging.info('%s > %s %s' % ('dict_s created in', t_end - t_start, 'seconds'))
        return jsonify(t_item_s), 200
    
    def post_option_s(self, p_source_id):
        t_start = perf_counter()
        t_data = json.loads(request.data)
        t_query = t_data['query']
        t_attr = t_data['attr']
        t_rel_attr = t_data['rel_attr']
        t_source = self.pool.__data__[p_source_id]
        t_option_s = t_source.model.get_option_s(t_query, t_attr, t_rel_attr)
        t_end = perf_counter()
        logging.info('%s > %s %s' % ('option_s created in', t_end - t_start, 'seconds'))
        return jsonify(t_option_s), 200
    
    def post_action(self, p_action_id):
        t_action = self.pool.__data__[p_action_id]
        t_data = dict()
        if request.data:
            t_data.update(json.loads(request.data))
        #OUT request.form wird nicht benötigt
        if request.form:
            t_data.update(json.loads(request.form['value']))
        if request.files:
            for key, value in request.files.items():
                # TODO - temporyry aus config.json verwenden
                t_path = Path('temporary').joinpath(value.filename)
                t_path.parent.mkdir(parents=True, exist_ok=True)
                value.save(t_path)
                t_data['item'][key] = t_path

        t_return = t_action.func(self.pool.__data__[t_action.source_id], t_data)

        if t_action.type == 'standard':
            return {'success': t_return[0], 'result': str(t_return[1])}, 200

        elif t_action.type == 'check':
            return {'success': t_return}, 200

        elif t_action.type == 'file':
            t_path = Path(t_return)
            return send_file(t_path, download_name=t_path.name)
        
    def get_query_s(self):
        def expand():
            for i_query in t_query_s:
                i_query['children'] = []
                for i2_query in t_query_s:
                    if i2_query['parent'] and i_query['id'] == i2_query['parent']['id']:
                        i_query['children'].append(i2_query)

        t_query_s = []
        for i_query in Decore_query.select():
            t_query_s.append(model_to_dict(i_query))

        expand()

        return jsonify(t_query_s)
    
    def post_save_query(self, p_base_id, p_view_id):

        # TODO - sorted DICT wieder einsetzen - p_query = OrderedDict(sorted((json.loads(request.data)).items()))
        p_query = json.loads(request.data)

        def get_url_query():
            if t_parent.id:
                r_parent_to:dict = json.loads(t_parent.to)
                r_parent_to['query'][i_query_key] = i_query_value
                return r_parent_to
            elif not t_parent.id:
                return {'path': '/' + p_base_id + '/' + p_view_id, 'query': {i_query_key: i_query_value}}

        # def get_title():
        #     t_title_key = ''
        #     t_title_value = i_query_value

        #     i_view: Decore_view
        #     for i_view in self.view_s:
        #         if p_view_id == i_view.id:
        #             t_model = self.get_base_by_id(i_view.source_id).model
        #             for i_field_key, i_field_value in t_model._meta.fields.items():
        #                 if i_query_key == i_field_key:
        #                     t_title_key = i_field_value.verbose_name
        #                     if 'ForeignKeyField' in str(i_field_value.__class__):
        #                         t_title_value = i_field_value.rel_model.get(
        #                             i_field_value.rel_model.id == i_query_value).title

        #     return t_title_key+"="+t_title_value

        t_parent = Decore_query()

        for i_query_key, i_query_value in p_query.items():
            # TODO - t_item = Decore_query.get_or_none(Decore_query.parent_id == t_parent.id and Decore_query.base_id == p_base_id and Decore_query.view_id == p_view_id and Decore_query.key == key and Decore_query.value == value)
            t_item = None
            i_item: Decore_query
            for i_item in Decore_query.select():
                if i_item.base_id == p_base_id:
                    if i_item.view_id == p_view_id:
                        if i_item.key == i_query_key:
                            if json.loads(i_item.value) == i_query_value:
                                if i_item.parent_id == t_parent.id:
                                    t_item = i_item

            if not t_item:
                t_item = Decore_query()
                t_item.id = str(uuid1())
                t_item.parent = t_parent
                t_item.base_id = p_base_id
                t_item.view_id = p_view_id
                t_item.title = str(i_query_key +':'+ str(i_query_value))
                t_item.key = i_query_key
                t_item.value = json.dumps(i_query_value)
                t_item.to = json.dumps(get_url_query())
                t_item.depth = t_parent.depth + 1 if t_parent.id else 0
                if t_item.save(force_insert=True):
                    t_parent = t_item
                else:
                    return 'error', 200
            elif t_item:
                t_parent = t_item

        return 'success', 200


    def get_remove_query(self, p_id):
        t_query_item = Decore_query.get_or_none(Decore_query.id == p_id)
        if t_query_item:
            t_query_item.delete_instance(recursive=True, delete_nullable=True)
            return 'success', 200
        else:
            return 'error', 200
        
decore = Decore()

# @api.route('/get_uniform')
# def get_uniform():
#     t_uniform = uniform.export()
#     t_uniform['csrf_token'] = generate_csrf()
#     return jsonify(t_uniform), 200

# @api.route('/element/<p_widget_id>/<p_element_id>', methods=['POST'])
# def element(p_widget_id, p_element_id):
#     t_widget = uniform.widget_s.get_by_id(p_widget_id)
#     t_element = t_widget.element_s.get_by_id(p_element_id)
#     t_data = json.loads(request.data)
#     t_return = t_element.func(uniform.get_base_by_module(t_element.func.__module__), t_data)
#     return json.dumps(t_return)