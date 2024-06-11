import inspect

from .decore_list import Decore_list
from .decore_fields import BackrefMetaField
from peewee import Field, BackrefAccessor, ManyToManyField


class Decore_object(object):

    t_ro_attr_s = [
        '_locked',
        'id',
        'parent_id',
        'role',
        'source_id',
    ]

    t_attr_s = [
        'activator',
        'active_s',
        'desc',
        'display',
        'errors',
        'filter_s',
        'hide',
        'icon',
        'id',
        'kind',
        'layout',
        'navigation',
        'pag_recs',
        'pag_type',
        'parent_id',
        'parent_kind',
        'private',
        'query',
        'stretch',
        'title',
        'type',
    ]

    def __init__(self, p_kind, p_id, p_parent_id, p_source_id, p_icon, p_title, p_desc, p_hide, p_role):
        self._locked = False
        self._mutated = True

        self.kind = p_kind
        self.parent_kind = None
        self.id = p_id
        self.parent_id = p_parent_id
        self.source_id = p_source_id
        self.icon = p_icon
        self.title = p_title
        self.desc = p_desc
        self.hide = p_hide
        self.role = p_role
        self.child_id_s = []

    def __setattr__(self, name, value):

        if hasattr(self, '_locked') and self._locked and name in self.t_ro_attr_s:
            raise Exception(name + ' is not changeable')

        if not name == '_mutated' and name in self.t_attr_s:
            self._mutated = True

        super().__setattr__(name, value)

    def export(self):
        self._mutated = False
        return self.serialize(self)

    def serialize(self, p_value):
        t_return = {}

        if type(p_value) is dict:
            for key, value in p_value.items():
                t_return[key] = self.serialize(value)

        elif Decore_object in inspect.getmro(p_value.__class__):
            # TODO - entferne class so allmählich aus dem gesamten Framework wir überprüfen ab dann über 'kind' und 'kind' wird direkt beim erstellen der klassen als attribut gesetzt.
            setattr(p_value, 'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                t_return[key] = self.serialize(value)

        elif BackrefMetaField in inspect.getmro(p_value.__class__):
            # TODO - isinstance gegen stringabfrage __name__ tauschen
            if hasattr(p_value.model, p_value.name) and (isinstance(getattr(p_value.model, p_value.name), BackrefAccessor) or isinstance(getattr(p_value.model, p_value.name), ManyToManyField)):
                p_value = getattr(p_value.model, p_value.name)

                if BackrefAccessor in inspect.getmro(p_value.__class__):
                    if hasattr(p_value.model, 'br_'+p_value.field.backref):
                        p_value.__dict__.update(
                            getattr(p_value.model, 'br_'+p_value.field.backref).__dict__)
                    setattr(p_value, 'class', p_value.__class__.__name__)
                    for key, value in p_value.__dict__.items():
                        t_return[key] = self.serialize(value)

                elif ManyToManyField in inspect.getmro(p_value.__class__):
                    if p_value._is_backref:
                        if hasattr(p_value.model, 'br_'+p_value.name):
                            p_value.__dict__.update(
                                getattr(p_value.model, 'br_'+p_value.name).__dict__)
                    setattr(p_value, 'class', p_value.__class__.__name__)
                    for key, value in p_value.__dict__.items():
                        t_return[key] = self.serialize(value)

            else:
                setattr(p_value, 'class', p_value.__class__.__name__)
                for key, value in p_value.__dict__.items():
                    t_return[key] = self.serialize(value)

        elif BackrefAccessor in inspect.getmro(p_value.__class__):
            if hasattr(p_value.model, 'br_'+p_value.field.backref):
                p_value.__dict__.update(
                    getattr(p_value.model, 'br_'+p_value.field.backref).__dict__)
            setattr(p_value, 'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                t_return[key] = self.serialize(value)

        elif ManyToManyField in inspect.getmro(p_value.__class__):
            if p_value._is_backref:
                if hasattr(p_value.model, 'br_'+p_value.name):
                    p_value.__dict__.update(
                        getattr(p_value.model, 'br_'+p_value.name).__dict__)
            setattr(p_value, 'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                t_return[key] = self.serialize(value)

        elif Field in inspect.getmro(p_value.__class__):
            setattr(p_value, 'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                t_return[key] = self.serialize(value)

        # TODO - depricated - Decore_list wird nicht mehr benötigt - entferne aus dem gesamten Framework
        elif Decore_list in inspect.getmro(p_value.__class__):
            t_list = []
            for value in p_value:
                t_list.append(self.serialize(value))
            return t_list

        elif type(p_value) is list:
            t_list = []
            for value in p_value:
                t_list.append(self.serialize(value))
            return t_list

        elif type(p_value) is str or type(p_value) is bool or type(p_value) is int:
            return p_value

        elif not p_value:
            return None

        else:
            return str(p_value)

        return t_return
