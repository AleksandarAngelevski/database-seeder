def seed_employee_type(curr, data=None):
   curr.executemany(
       """
        INSERT INTO EMPLOYEETYPE (type, permissions)
        VALUES (%s, %s)
        ON CONFLICT (type) DO NOTHING  
                """,
[
            ("Waiter",0,),
            ("Manager",1,),
            ("Supervisor",2,),
            ("Admin", 4,),
            ("Host", 3,),
            ]
        ) 
