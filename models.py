from faker import Faker
import random
fake = Faker('ar_SA') 
def generate_employee():
    employment_date = fake.date_between(start_date='-5y', end_date='today')
    
    # 60% chance still employed
    if random.random() < 0.6:
        resignation_date = None
    else:
        resignation_date = fake.date_between(start_date=employment_date, end_date='today')
    
    sex = random.choice(['M', 'F'])
    first_name = fake.first_name_male() if sex == 'M' else fake.first_name_female()
    last_name = fake.last_name_male() if sex == 'M' else fake.last_name_female() 



    return (
            first_name, 
            last_name,
            fake.unique.numerify("#############"),
            sex,
            fake.unique.email(),
            fake.sha256(),
            employment_date,
            resignation_date)



def generate_employee_type():
    return [
            ("Waiter",0),
            ("Manager",1),
            ("Supervisor",2),
            ("Admin", 4)
            ]
