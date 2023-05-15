from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.company_model import Company_model as Model

@decore.base(p_title='Companies', p_model=Model)
class Company_base(Base):
    
    @decore.widget(p_parent_id='per_vi1_di1_wi1', p_title='Companies', p_type='table', p_active_s=Model.field_s)
    def per_vi1_di1_wi1_wi2():
        pass