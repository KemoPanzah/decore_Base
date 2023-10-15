from peewee import (AutoField, BooleanField, CharField, DateTimeField, Model,
                    SqliteDatabase)


class Decore_mayor(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = SqliteDatabase('state/mayorbase.db')

    # Funktion um die Tabelle zu erstellen und die Klasse zurückzugeben
    @classmethod
    def register(cls):
        cls.create_table(safe=True)
        if cls.get_or_none(cls.username == 'guest') is None:
            guest = cls()
            guest.username = 'guest'
            guest.password = 'guest'
            guest.save()
        return cls
    
