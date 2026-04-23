import os
import random
from dotenv import load_dotenv
def seed_employee_role(curr):
    load_dotenv()
    employee_size = int(os.getenv("EMPLOYEE_COUNT",0))
    employee_type_size = int(os.getenv("EMPLOYEE_TYPES_COUNT",0))
    for i in range(employee_size): 
        curr.execute("""
                     INSERT INTO EMPLOYEEROLE (EmployeeId, EmployeeTypeId)
                     VALUES(%s, %s)
                     """, (i+1,random.randint(1,employee_type_size),))
        print(f"\rSeeding employee roles: {((i+1)/employee_size*100):.1f}%", end="", flush=True)
    print()
