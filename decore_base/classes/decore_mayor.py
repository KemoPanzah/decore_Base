from peewee import (AutoField, BooleanField, CharField, DateTimeField, Model,
                    SqliteDatabase)


class decore_Mayor(Model):
    id = AutoField(primary_key=True)
    username = CharField()
    password = CharField()

    class Meta:
        database = SqliteDatabase('state/mayorbase.db')

    # Funktion um die Tabelle zu erstellen und die Klasse zurückzugeben
    @classmethod
    def register(cls):
        cls.create_table(safe=True)
        return cls
    
    