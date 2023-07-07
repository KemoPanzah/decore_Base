from pykeepass import create_database, PyKeePass
from pykeepass.entry import Entry
from uuid import uuid4

class Meta_item:
    def __init__(self, p_uuid, p_group, p_title, p_username, p_password):
        self.uuid = p_uuid
        self.group = p_group
        self.title = p_title
        self.username = p_username
        self.password = p_password

class Global_keybase(PyKeePass):
    
    __meta__ = {}

    def __init__(self, keybase_path):
        keybase_path.parent.mkdir(parents=True, exist_ok=True)
        if not keybase_path.exists():
            create_database(str(keybase_path.absolute()), password='12345678')
        PyKeePass.__init__(self, keybase_path, password='12345678')
    
    def append(self, p_group, p_title, p_username, p_password):
        
        t_group = self.find_groups_by_name(p_group, group=self.root_group, first=True)
        
        # MEMO - Prüfe ob der Eintrag bereits in der keybase vorhanden ist wenn ja speichere die Aktualisieung in der Meta
        if t_group:            
            i_entry: Entry
            for i_entry in t_group.entries:
                if p_title == i_entry.title and p_username == i_entry.username:
                    if not p_password == i_entry.uuid.hex:
                        self.__meta__[i_entry.uuid.hex] = Meta_item(i_entry.uuid, p_group, p_title, p_username, p_password)
                    return i_entry.uuid.hex
        # MEMO - Überprüfe ob der Eintrag bereits in der Meta vorhanden ist und aktualisiere ihn
        i_meta_item: Meta_item
        for i_meta_item in self.__meta__.values():
            if i_meta_item.title == p_title and i_meta_item.username == p_username:
                i_meta_item.title = p_title
                i_meta_item.username = p_username
                i_meta_item.password = p_password
                return i_meta_item.uuid.hex
        # MEMO - Wenn Eintrag nicht in keybase oder Meta vorhanden ist, erstelle ihn
        t_uuid = uuid4()
        self.__meta__[t_uuid.hex] = Meta_item(t_uuid, p_group, p_title, p_username, p_password)
        return t_uuid.hex

    def get_entry(self, p_group, p_password):
        i_meta_item: Meta_item
        for i_meta_item in self.__meta__.values():
            if p_password == i_meta_item.uuid.hex:
                return i_meta_item.password

        t_entry = None
        t_group = self.find_groups_by_name(p_group, group=self.root_group, first=True)
        if t_group:
            # MEMO - Suche nach einem Eintrag der dem Identifiziern entspricht und gebe das Password des Eintrages zurück
            i_entry: Entry
            for i_entry in t_group.entries:
                if i_entry.uuid.hex == p_password:
                    return i_entry.password
            
            # MEMO - Wenn kein Eintrag vorhanden ist, gebe None als Passwort aus
            if not t_entry:
                return None
        else:
            return None

    def commit(self, instance_id):
        t_meta_item: Meta_item
        for t_meta_item in self.__meta__.values():
            if t_meta_item.title == instance_id:
                t_entry = None
                t_group = self.find_groups_by_name(t_meta_item.group, group=self.root_group, first=True)
                if not t_group:
                    t_group = self.add_group(self.root_group, t_meta_item.group)
                
                # MEMO - Suche nach einem Eintrag der dem Identifiziern entspricht und ändere gegenebenenfalls das Passwort
                i_entry: Entry
                for i_entry in t_group.entries:
                    if t_meta_item.title == i_entry.title and t_meta_item.username == i_entry.username:
                        t_entry = i_entry
                        # MEMO - Wenn der neue Wert nicht mit dem Password im Entry übereinstimmt und auch nicht mit der UUID dann ändere und speichere
                        if not t_meta_item.password == t_entry.password:
                            t_entry.password = t_meta_item.password
                
                # MEMO - Wenn kein Eintrag vorhanden ist, lege einen neuen an und füge diesen der Gruppe hinzu
                if not t_entry:
                    t_entry = Entry(title='none', username='none', password='none',kp=self)
                    t_entry.uuid = t_meta_item.uuid
                    t_entry.title = t_meta_item.title
                    t_entry.username = t_meta_item.username
                    t_entry.password = t_meta_item.password
                    t_group.append(t_entry)

        # MEMO - Speichere die Änderungen        
        try:
            self.save()
            self.__meta__ = {}
            return True
        except:
            raise Exception('Could not save to keybase')