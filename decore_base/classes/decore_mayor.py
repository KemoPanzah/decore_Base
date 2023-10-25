from flask_jwt_extended import create_access_token
import bcrypt

from ..models.bi_account_model import BI_Account_model as Model

class Decore_mayor:    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def login(self, username, password):
        t_account = Model.get_or_none(Model.username == username)
        if t_account is None:
            return None
        elif self.check_password(password, t_account.password):
            return create_access_token(identity=t_account.username)