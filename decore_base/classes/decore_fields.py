from uuid import UUID

from peewee import CharField, Field, UUIDField


class DecoreUUIDField(UUIDField):
    def __init__(self, *args, **kwargs):
        UUIDField.__init__(self, *args, **kwargs)
    
class DecoreCharField(CharField):
    def __init__(self, *args, **kwargs):
        CharField.__init__(self, *args, **kwargs)