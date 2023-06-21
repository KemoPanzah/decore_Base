from decore_base import decore
from models.person_model import Person_model
from models.account_model import Account_model
from models.company_model import Company_model


from mimesis import Person, Finance
from random import randrange

@decore.base(title='Global Management', icon='mdi-account-supervisor-circle-outline')
class Global_management_base:
    def __init__(self):
        self.test_attr = 'test_attr'
        pass

    @decore.function(type='shot')
    def create_data(self):
        self.test_item()
        self.query_tester()
        self.create_company_s()
        self.create_person_s()
        # self.set_company_person()
    
    def test_item(self):
        t_account = Account_model()
        t_account.title = 'test'
        t_account.email = 'test@mail.com'
        t_account.password = 'test'
        t_account.save()
        t_account_s = list(Account_model.select())
        pass

    # Query tester
    def query_tester(self):
        t_item_s = Person_model.query({'companies__title__eq':'NetApp'})
        pass

    # Create 32 companies with capacity 16-128 of persons
    def create_company_s(self):
        while len(Company_model.select()) < 32:
            t_finance = Finance()
            t_item = Company_model()
            t_item.title = t_finance.company()
            t_item.capacity = randrange(16, 128)
            t_item.save()

    # Create 4096 persons with capacity 1-2 of companies
    def create_person_s(self):        
        while len(Person_model.select()) < 32:
            t_item = Person_model()
            t_item.title = t_item.first_name + ' ' + t_item.last_name
            t_item.save()

    # Set persons to companies
    def set_company_person(self):
        for company in Company_model.select():
            while company.persons.count() < company.capacity:
                t_person_num = randrange(Person_model.select().count())
                t_person_item = Person_model.select()[t_person_num]
                if t_person_item.companies.count() < t_person_item.capacity:
                    b_found = False
                    for company_person in company.persons:
                        if t_person_item.id == company_person.id:
                            b_found = True
                    if not b_found:
                        company.persons.add(t_person_item)

    # @decore.function(p_type='init')
    # def create_account_s(self):
    #     for i_person in Person_model.select():
    #         t_person = Person()
    #         t_item = Account_model.get_or_none(Account_model.person == i_person)
    #         if not t_item:
    #             t_item = Account_model()
    #             t_item.id = t_item.create_uuid()
    #             t_item.person = i_person
    #             t_item.email = t_person.email()
    #             t_item.title = t_item.email
    #             t_item.password = t_person.password()
    #             t_item.save()