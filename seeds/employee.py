from models import generate_employee
def seed_employee(curr,n = 10):
    for i in range(n):
        
        curr.execute(
                """
                INSERT INTO EMPLOYEE (FirstName, LastName, SSN, Sex, Email, PasswordHash, DateEmployment, DateResignation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                ,
                generate_employee()
                ) 

        print(f"\rSeeding employee: {((i+1)/n*100):.1f}%",end="", flush=True)
    print()
