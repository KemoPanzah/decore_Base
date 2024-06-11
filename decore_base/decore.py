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
from .classes.decore_template import Decore_template
from .classes.decore_hook import Decore_hook
from .classes.decore_prompt import Decore_prompt
from .classes.decore_mayor import Decore_mayor as Mayor
from .classes.decore_actor import Decore_actor
from .classes.decore_route import Decore_route

from . import globals

from playhouse.shortcuts import model_to_dict
from uuid import uuid1
from typing import Literal
from time import perf_counter

from flask import Flask, render_template, request, jsonify, send_file, render_template_string
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

import json, logging
from str2type import str2type
from pathlib import Path
from collections import OrderedDict


class Decore(object):
    '''
    Objekt der Klasse Decore ist die Hauptklasse des Frameworks. Sie ist für die Registrierung der Elemente zuständig und stellt die API zur Verfügung.
    '''
    def __init__(self):
        if not globals.flags.production_mode:
            self.prompt = Decore_prompt()
        self.pool = Decore_pool()
        self.actor = Decore_actor.register()
        self.api = self.get_api()
        Decore_query.create_table(safe=True)
        
    def get_api(self):
        t_static_folder = Path('spa/static')
        t_template_folder = Path('spa/templates')
        api = Flask(__name__, static_folder=t_static_folder.absolute(), template_folder=t_template_folder.absolute())

        # TODO - CRSF implementation
        # TODO - Alle Requests mit verschlüsseltem HASH versehen und auf der Client-Seite entschlüsseln und prüfen

        # TODO - jwt String auslagern und aus der Versionskontrolle nehmen, oder ein zufälligen in der config generieren
        api.config['JWT_SECRET_KEY'] = 'super-secret'
        JWTManager(api)
        
        if globals.flags.dev_mode:
            # CORS(api, expose_headers=["Content-Disposition"])
            CORS(api)
            logging.info('CORS enabled while in development mode')

            
        # print('APP_ROOT_FOLDER >> ' + str(api.root_path))
        # print('STATIC_FOLDER >> ' + str(api.static_folder))
        # print('TEMPLATE_FOLDER >> ' + str(api.template_folder))
        api.add_url_rule('/', 'index', self.index, defaults={'p_path': ''})
        api.add_url_rule('/<path:p_path>', 'index', self.index)
        api.add_url_rule('/guest_login', 'guest_login', self.guest_login, methods=['POST'])
        api.add_url_rule('/get_meta', 'get_meta', self.get_meta)
        api.add_url_rule('/post_item/<p_source_id>/<p_item_id>', 'post_item', self.post_item, methods=['POST'])
        api.add_url_rule('/post_item_s/<p_source_id>', 'post_item_s', self.post_item_s, methods=['POST'])
        api.add_url_rule('/post_rel_item_s/<p_source_id>', 'post_rel_item_s', self.post_rel_item_s, methods=['POST'])
        api.add_url_rule('/post_filter_value_s/<p_source_id>', 'post_filter_value_s', self.post_filter_value_s, methods=['POST'])
        api.add_url_rule('/post_action/<p_action_id>', 'post_action', self.post_action, methods=['POST'])
        api.add_url_rule('/get_query_s', 'get_query_s', self.get_query_s)
        api.add_url_rule('/post_save_query/<p_base_id>/<p_view_id>', 'post_save_query', self.post_save_query, methods=['POST'])
        api.add_url_rule('/get_remove_query/<p_id>', 'get_remove_query', self.get_remove_query)
        api.add_url_rule('/get_actor_active_s', 'get_actor_active_s', self.get_actor_active_s)
        api.add_url_rule('/get_actor_item_s', 'get_actor_item_s', self.get_actor_item_s)
        api.add_url_rule('/get_template/<p_template_id>', 'get_template', self.get_template)
        api.add_url_rule('/get_hook/<p_hook_id>', 'post_hook', self.get_hook)
        return api

    def start_api(self):
        import os, sys
        from waitress import serve
        HOST = os.environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(os.environ.get('SERVER_PORT', str(globals.config.app_port)))
        except ValueError:
            PORT = globals.config.app_port
        
        if not globals.flags.dev_mode:
            logger = logging.getLogger('waitress')
            logger.info(self.pool.app.title + ' now running on: http://' + str(HOST) + ':' + str(PORT))
            logger.info('Press CTRL+C to quit.')
            logger.setLevel(logging.WARNING)
            serve(self.api, host=HOST, port=PORT, threads=32)
            
        else:
            self.api.run(HOST, PORT)

    # TODO - allow_guest gegen role tauschen role=1 ist allow_guest
    def app(self, title, desc=None, role=1):
        '''
        Eine Funktion zum eröffnen einer GUI-Dashboard-Anwendung. Sie wird als "Decorator" verwendet.

        :param str title: Der Titel der App.
        :param bool allow_guest: Gibt an, ob der Gastzugang (Anonynus) erlaubt ist. Der Wert ``True`` erlaubt den automatischen Login als Gast. Der Wert ``False`` verweigert das senden der Metadaten an das Frontend und verweist auf die Login-Seite.

        .. code-block:: python

            @decore.app(title='My App', allow_guest=False)
            def main():
                pass
        '''
        def wrapper(func):
            self.pool.register(Decore_app(title, desc, role))
            self.pool.extend()
            self.pool.set_roles(self.pool.__data__['app'])
            self.pool.lock_objects()

            i_base: Decore_base
            for i_base in self.pool.base_s:
                i_base.rel_field_s = i_base.model.rel_field_s
                i_base.start_shot()
                i_base.start_work()
            self.start_api()
        return wrapper

    l_base_navigation = Literal['main-top', 'main-bottom']
    def base(self, icon=None, title=None, desc=None, hide=False, role=1, model=Decore_model, private=False, stretch=False, navigation: l_base_navigation='main-top'):
        '''
        Eine Funktion zum registrieren einer Basis in der GUI-Dashboard-Anwendung. Sie wird als "Decorator" verwendet.

        Die Basis ist das Trägerelement für die Ansicht und die Vorlage für die Datenquelle im Frontend.

        :param str icon: Das Symbol der Basis.
        :param str title: Der Titel der Basis.
        :param str desc: Die Beschreibung der Basis.
        :param Model model: Das Datenmodell der Basis.

        .. code-block:: python

            @decore.base(icon='mdi-account', title='Person', desc='A basis for managing personal data', model=Person)
            class Person_base:
                pass
        '''
        def wrapper(cls):
            t_base = Decore_base(cls.__name__, icon, title, desc, hide, role, model, private, stretch, navigation)
            t_base.__class__ = type(cls.__name__, (Decore_base, cls), {
                '__init__': cls.__init__(t_base),
            })
            self.pool.register(t_base)
        return wrapper

    l_view_type = Literal['default', 'table']
    l_view_pag_type = Literal['client']

    def view(self, parent_id=None, icon=None, title=None, desc=None, hide=False, role=1, type: l_view_type = 'default', fields=[], filters=[], query={}, pag_type: l_view_pag_type = 'client', pag_recs=16):
        '''
        Eine Funktion zur Registrierung einer Ansicht. Sie wird als "Decorator" verwendet.

        Eine Ansicht ist ein Container für die Anzeige von Daten.
        
        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn die Ansicht in einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol der Ansicht.
        :param str title: Der Titel der Ansicht.
        :param str desc: Die Beschreibung der Ansicht.
        :param str type: Gibt an wie die Datensätze angezeigt werden. Der Wert ``table`` stellt die Datensätze in einer Tabelle dar.
        :type type: Literal['default']
        :param list fields: Die Felder, die in der Ansicht angezeigt werden.
        :param list filters: Die Filter, die in der Ansicht angezeigt werden.
        :param dict query: Die Abfrage, die in der Ansicht angezeigt wird.
        :param str pag_type: Wählt die Methode wie die Datensätze der View geladen werden. Der Wert ``client`` lädt alle Datensätze auf einmal und überlässt den Seitenaufbau dem Frontend.
        :type pag_type: Literal['client']
        :param int pag_recs: Gibt an wieviele Datensätze auf einer Seite der Ansicht angezeigt werden sollen. ``16`` ist die Standardeinstellung.

        .. code-block:: python

            @decore.view(icon='mdi-account', title='Person', desc='A view for managing personal data', type='table', fields=[Person.id, Person.name, Person.age], filters=[Person.name, Person.age], query={'name__eq': 'Kemo'}, pag_type='client', pag_recs=16)
            def person_view():
                pass
        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_view(func.__name__, t_parent_id, t_source_id, icon, title, desc, hide, role, type, fields, filters, query, pag_type, pag_recs))
            func()
        return wrapper

    l_dialog_type = Literal['standard']
    l_dialog_display = Literal['modal', 'draw-half', 'draw-full']
    l_dialog_activator = Literal['empty', 'first', 'last', 'default', 'context', 'click']

    # TODO - Überprüfen ob element mit gleicher ID schon vorhanden ist und Execption
    def dialog(self, parent_id=None, icon=None, title=None, desc=None, hide=False, role=1, type: l_dialog_type = 'standard', display: l_dialog_display = 'draw-half', activator: l_dialog_activator = 'empty'):
        '''
        Eine Funktion zur Registrierung eines Dialogs. Sie wird als "Decorator" verwendet.

        Der Dialog ist das Trägerelement für Widgets 

        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn der Dialog in einer Ansicht einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol des Dialogs.
        :param str title: Der Titel des Dialogs.
        :param str desc: Die Beschreibung des Dialogs.
        :param str type: Gibt an wie der Dialog die Widgets darstellen wird. Der Wert ``standard`` stellt die untergeordneten Widgets und Sub-Widgets untereinander dar.
        :type type: Literal['standard']
        :param str display: Der Anzeigetyp des Dialogs. Standardwert ist ``draw-half``.
        :type display: Literal['modal', 'draw-half', 'draw-full']
        :param str activator: Der Aktivatortyp des Dialogs. Über den Wert ``none`` wird der Dialog sofort beim OnLoad Ereignis der View angezeigt. Der Wert ``default`` stellt den Dialog im Top-Menu der View dar. Der Wert ``context`` stellt den Dialog im Kontextmenü eines Items der View dar. Der Wert ``click`` zeigt den Dialog dann an wenn man einen Datensatz anklickt.
        :type activator: Literal['none', 'default', 'context', 'click']

        .. code-block:: python

            @decore.dialog(icon='mdi-account', title='Person', desc='A dialog for managing personal data', type='standard', display='drawer', activator='default-menu')
            def person_dialog():
                pass
                
        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_dialog(func.__name__, t_parent_id, t_source_id, icon, title, desc, hide, role, type, display, activator))
            func()
        return wrapper

    l_widget_type = Literal['default', 'info', 'form', 'table']

    def widget(self, parent_id=None, icon=None, title=None, desc=None, hide=False, role=1, type: l_widget_type = 'default', layout='ceta', fields=[]):
        '''
        Eine Funktion zur Registrierung eines Widgets. Sie wird als "Decorator" verwendet.

        Ein Widget dient zur Darstellung und Interaktion mit dem Datensatz. Es erhält die Daten, die der Dialog-Aktivator vorgibt. Der Wert ``none`` übergibt den letzten Datensatz der Datenbanktabelle. Der Wert ``default`` übergibt einen nur mit Default-Werten gefüllten Datensatz. Beim Wert ``context`` übergibt es den Datensatz, der im Kontextmenü der Ansicht ausgewählt wurde. Und ``click`` übergibt den Datensatz, der angeklickt wurde. 

        Widgets, welche aus einer fremden Basis einem Dialog zugeordnet werden, ergänzen die relationalen Felder eines Default-Items der fremden Datenquelle mit den Daten des aktivierten Items. (Der Satz ist Scheiße zu verstehen, aber er trifft genau das, was es tut). In der Sample Anwendung verwende ich das beim Zuweisen von "Contracts" zu einer "Person". 

        Es gibt aber auch Widgets, die mehrere Datensätze darstellen können, wie im Beispiel davor werden hier auch die Relationen verwendet, um nur Daten abzubilden, die etwas mit dem gewählten Item zu tun haben.

        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn das Widget in einem Dialog einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol des Widgets.
        :param str title: Der Titel des Widgets.
        :param str desc: Die Beschreibung des Widgets.
        :param str type: Gibt an wie das Widget die Daten darstellen wird. Standardwert ist ``default``.
        :type type: Literal['default', 'info', 'form', 'table']
        :param list fields: Die Felder, die in dem Widget angezeigt werden.

        .. code-block:: python
        
            @decore.widget(icon='mdi-account', title='Person', desc='A widget for managing personal data', type='form', layout='cera', fields=[Person.name, Person.age])
            def person_widget():
                pass
                
        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_widget(func.__name__, t_parent_id, t_source_id, icon, title, desc, hide, role, type, layout, fields))
            func()
        return wrapper

    def template(self, parent_id=None, icon=None, title=None, desc=None, hide=False, role=1):
        '''
        Eine Funktion zur Registrierung einer Vorlage. Sie wird als "Decorator" verwendet.

        Eine Vorlage ist HTML-Code der im Layout der View oder des Widgets gerendert wird.

        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn die Vorlage in einem Dialog einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol der Vorlage.
        :param str title: Der Titel der Vorlage.
        :param str desc: Die Beschreibung der Vorlage.
        :param str name: Der Name der Vorlage.

        .. code-block:: python

            @decore.template(icon='mdi-account', title='Person', desc='A html template', name='person_template')
            def person_template():
                pass
        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_template(func.__name__, t_parent_id, t_source_id, icon, title, desc, hide, role, func))
        return wrapper
    
    def hook(self, parent_id=None, icon=None, title=None, desc=None, role=1):
        '''
        Eine Funktion zur Registrierung eines "Hakens". Sie wird als "Decorator" verwendet. 

        Ein Haken ist eine Funktion zum abfangen von Ereignissen aus dem Frontend. Es wird immer dann ausgeführt, wenn ein beliebiges Ereignis eintritt, sofern sie definiert ist.

        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn der Haken in einem Dialog einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol des Hakens.
        :param str title: Der Titel des Hakens.
        :param str desc: Die Beschreibung des Hakens.
        :param str name: Der Name des Hakens.

        .. code-block:: python
            
            @decore.hook(icon='mdi-account', title='Person', desc='A hook to catch events')
                pass

        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_hook(func.__name__, t_parent_id, t_source_id, icon, title, desc, role, func))
        return wrapper

    l_action_type = Literal['standard', 'submit']
    l_action_activator = Literal['default', 'context', 'click']

    def action(self, parent_id=None, icon=None, title=None, desc=None, hide=False, role=1, type: l_action_type = 'standard', activator: l_action_activator = 'none', errors=True):
        '''
        Eine Funktion zur Registrierung einer Aktion. Sie wird als "Decorator" verwendet.

        Eine Aktion ist die tatsächliche Interaktion zwischen dem Benutzer und dem Backend.

        :param str parent_id: Die ID des übergeordneten Elements. Nur zu setzen, wenn die Aktion in einem Widget einer anderen Basis gerendert werden soll.
        :param str icon: Das Symbol der Aktion.
        :param str title: Der Titel der Aktion.
        :param str desc: Die Beschreibung der Aktion.
        :param str type: Gibt an was die Aktion kann. Standardwert ist ``standard``.
        :type type: Literal['standard', 'submit']
        :param str activator: Gib an, wie die Aktion ausgelöst wird.
        :type activator: Literal['default', 'context', 'click']
        :param bool errors: Gibt an, ob die Aktion Validierungsfehler zurückgeben kann. Standardwert ist ``True``. (Im Augenblick wirkt sich das nur auf den Typen ``submit`` aus.)

        .. code-block:: python
            
            @decore.action(icon='mdi-account', title='Person', desc='A action for managing personal data', type='submit')
            def sample_action(item, **kwargs):
                pass
        
        Die Aktionen durchlaufen ein Modul, welches die erhaltenen Daten aufbereitet und als Keyword-Parameter an die dekorierte Funktion übergibt. Es ist alles in den ``kwargs`` zu finden und man macht sich diese einfach verfügbar. Der Parameter ``item`` ist ein Beispiel dafür und repräsentiert den vom Frontend zurückgegebenen Datensatz. Um herauszufinden, was alles noch in den ``kwargs`` steckt, bitte den Debugger benutzen.
        '''

        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            if not parent_id:
                t_parent_id = t_parent_s[-2]
            else:
                t_parent_id = parent_id
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_action(func.__name__, t_parent_id, t_source_id, icon, title, desc, hide, role, type, activator, errors, func))
        return wrapper

    # l_element_type = Literal['p', 'checkbox']

    # def element(self, parent_id=None, icon=None, title=None, desc=None, role=0, type: l_element_type = 'text', default=None, disable=False, schema=None):
    #     def wrapper(func):
    #         t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
    #         if not parent_id:
    #             t_parent_id = t_parent_s[-2]
    #         else:
    #             t_parent_id = parent_id
    #         t_source_id = t_parent_s[0]
    #         self.pool.register(Decore_element(func.__name__, t_parent_id, t_source_id, icon, title, desc, role, type, default, disable, schema, func))
    #     return wrapper

    l_function_type = Literal['shot', 'work']
  
    def function(self, type:l_function_type = 'shot'):
        '''
        Eine Funktion zur Registrierung einer Funktion in der übergeordneten Base. Sie wird als "Decorator" verwendet.

        Eine Funktion wird direkt nach der Zusammenstellung des Metadaten-Pool ausgeführt. Mit Funktionen kann man die Logik erweitern, Dinge vorbereiten oder Hintergrundaufgaben erledigen. Sie agieren als Instanzmethoden der Basis und erhalten damit den objektorientierten Ansatz.

        :param str type: Gibt an wie eine Funktion ausgeführt wird. Mit dem Wert ``shot`` wird sie nur einmal ausgeführt. Der Wert ``work`` wird in einem Thread ausgeführt und kann somit Schleifen abarbeiten die niemals enden bis der Main-Thread endet.
        :type type: Literal['shot', 'work']

        .. code-block:: python
            
            @decore.function(type='shot')
            def sample_function(self):
                pass
        '''
        def wrapper(func):
            t_parent_s = func.__qualname__.replace('.<locals>', '').rsplit('.')
            t_parent_id = t_parent_s[-2]
            t_source_id = t_parent_s[0]
            self.pool.register(Decore_function(func.__name__, t_parent_id, t_source_id, None, None, None, type, func))
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
    
    def guest_login(self):
        t_username = request.json['username']
        t_password = request.json['password']
        t_token = Mayor.get_token(t_username, t_password, False)
        if t_token:
            return {'success': True, 'result': 'Login successfully', 'token': t_token, 'errors':{}}, 200
        else:
            return {'success': False, 'result':'Invalid username or password', 'token': None, 'errors':{}}, 401

    @jwt_required()
    def get_meta(self):
        t_identity = get_jwt_identity()
        t_role = Mayor.get_account_from_identity(t_identity).role
        t_return = json.dumps(self.pool.export(t_role), default=str)
        return t_return, 200
    
    @jwt_required()
    def post_item(self, p_source_id, p_item_id):
        t_jwt_user_id = Mayor.get_account_from_identity(get_jwt_identity()).id
        t_query = request.json
        t_source = self.pool.__data__[p_source_id]
        if t_source.private:
            t_query['owner_id'] = t_jwt_user_id
        t_item = t_source.model.get_dict(p_item_id, t_query)
        t_return = json.dumps(t_item, default=str)
        return t_return, 200

    @jwt_required()    
    def post_item_s(self, p_source_id):
        t_start = perf_counter()
        # TODO - Umstellen auf request.json - Das ist viel schöner.
        t_query = json.loads(request.data)
        t_source = self.pool.__data__[p_source_id]
        t_item_s = t_source.model.get_dict_s(t_query)
        t_end = perf_counter()
        logging.info('%s > %s %s' % ('dict_s created in', t_end - t_start, 'seconds'))
        t_return = json.dumps(t_item_s, default=str)
        return t_return, 200
    
    def post_rel_item_s(self, p_source_id):
        # TODO - Umstellen auf request.json - Das ist viel schöner.
        t_query = json.loads(request.data)
        t_source = self.pool.__data__[p_source_id]
        t_return = json.dumps(t_source.model.get_minified_dict_s(t_query), default=str)
        return t_return, 200

    def post_filter_value_s(self, p_source_id):
        # TODO - Umstellen auf request.json - Das ist viel schöner.
        t_data = json.loads(request.data)
        t_query = t_data['query']
        t_attr = t_data['attr']
        t_rel_attr = t_data['rel_attr']
        t_source = self.pool.__data__[p_source_id]
        t_option_s = t_source.model.get_attributed_value_s(t_query, t_attr, t_rel_attr)
        t_return = json.dumps(t_option_s, default=str)
        return t_return, 200

    @jwt_required()
    def post_action(self, p_action_id):
        t_action = self.pool.__data__[p_action_id]
        # TODO - t_object > t_parent
        t_object = self.pool.__data__[t_action.parent_id]
        t_user = Mayor.get_account_from_identity(get_jwt_identity())
        return self.actor.fire(self.pool.__data__[t_action.source_id], t_action, t_object, t_user, request)

        # t_data = dict()
        # if request.data:
        #     t_data.update(json.loads(request.data))
        # #OUT request.form wird nicht benötigt
        # if request.form:
        #     t_data.update(json.loads(request.form['value']))
        # if request.files:
        #     for key, value in request.files.items():
        #         # TODO - temporyry aus config.json verwenden
        #         t_path = Path('temporary').joinpath(value.filename)
        #         t_path.parent.mkdir(parents=True, exist_ok=True)
        #         value.save(t_path)
        #         t_data['item'][key] = t_path

        # t_return = t_action.func(self.pool.__data__[t_action.source_id], t_data)

        # if t_action.type == 'standard':
        #     return {'success': t_return[0], 'result': str(t_return[1])}, 200
        
        # if t_action.type == 'submit':
        #     return {'success': t_return[0], 'result': str(t_return[1])}, 200

        # elif t_action.type == 'check':
        #     return {'success': t_return}, 200

        # elif t_action.type == 'file':
        #     t_path = Path(t_return)
        #     return send_file(t_path, download_name=t_path.name)
        
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

        t_return = json.dumps(t_query_s, default=str)
        return t_return
    
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
        
    def get_actor_active_s(self):
        t_return = json.dumps(self.actor.export_active_s(), default=str)
        return t_return, 200
    
    def get_actor_item_s(self):
        t_return = json.dumps(self.actor.export_item_s(), default=str)
        return t_return, 200

    @jwt_required()
    def get_template(self, p_template_id):
        t_template = self.pool.__data__[p_template_id]
        t_base = self.pool.__data__[t_template.source_id]
        t_identity = get_jwt_identity()
        t_user = Mayor.get_account_from_identity(t_identity) 
        t_template_data = t_template.func(t_base, user=t_user)      
        t_return = render_template_string(t_template_data[0], **t_template_data[1])
        return t_return, 200
    
    @jwt_required()
    def get_hook(self, p_hook_id):
        t_hook = self.pool.__data__[p_hook_id]
        t_base = self.pool.__data__[t_hook.source_id]
        t_identity = get_jwt_identity()
        t_user = Mayor.get_account_from_identity(t_identity)
        t_route = Decore_route()
        t_hook.func(t_base, user=t_user, pool=self.pool.__data__, route=t_route)
        return {'meta': self.pool.export(t_user.role, 'mutated'), 'route': t_route.get()}, 200

decore = Decore()