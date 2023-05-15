from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.person_model import Person_model
from models.account_model import Account_model
from models.company_model import Company_model


from mimesis import Person, Finance
from random import randrange

@decore.base(p_title='Personal Management', p_icon='mdi-account-supervisor-circle-outline')
class Global_management_base(Base):
    
    # @decore.function(p_type='init')
    # def query_tester(self):
    #     from peewee import DQ
    #     t_person_s = list(Person_model.select())
    #     t_companie_s = list(Company_model.select())
    #     t_account_s = list(Account_model.select())
    #     t_item_s = Person_model.query({'last_name':'Glover', 'companies__title__eq':'CNA', 'accounts__title__eq':'upper2074@example.com'})
    #     t_or_chain = None
    #     t_or_key = 'academic_degree'
    #     t_or_chain |= DQ(**{t_or_key: 'Master'})
    #     # t_or_chain |= DQ(**{t_or_key: 'Master'})
    #     t_or_test = Person_model.filter(t_or_chain)
    #     pass

    @decore.function(p_type='init')
    def create_company_s(self):
        while len(Company_model.select()) < 25:
            t_finance = Finance()
            t_item = Company_model(t_item.create_id())
            t_item.title = t_finance.company()
            t_item.save()

    @decore.function(p_type='init')
    def create_person_s(self):        
        while len(Person_model.select()) < 50:
            t_person = Person()
            t_item = Person_model(t_item.create_id())
            t_item.first_name = t_person.first_name()
            t_item.last_name = t_person.last_name()
            t_item.title = t_item.first_name + ' ' + t_item.last_name
            t_item.academic_degree = t_person.academic_degree()
            t_item.age = t_person.age(minimum=18, maximum=70)
            t_item.save()

    @decore.function(p_type='init')
    def connect_company_person(self):
        for person in Person_model.select():
            t_company_num = randrange(Company_model.select().count())
            t_company_item = Company_model.select()[t_company_num]
            bfound = False
            for company_person in t_company_item.persons:
                if person.id == company_person.id:
                    bfound = True
            if not bfound:
                t_company_item.persons.add(person)

    @decore.function(p_type='init')
    def create_account_s(self):
        for i_person in Person_model.select():
            t_person = Person()
            t_item = Account_model.get_or_none(Account_model.person == i_person)
            if not t_item:
                t_item = Account_model(t_item.create_id())
                t_item.person = i_person
                t_item.email = t_person.email()
                t_item.title = t_item.email
                t_item.password = t_person.password()
                t_item.save()