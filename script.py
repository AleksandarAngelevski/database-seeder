from models import *
from seeds.employee_type import seed_employee_type
import psycopg2

conn = psycopg2.connect(
        dbname="test_advdb",
        user="postgres",
        host="localhost",
        port=5432
        )

curr = conn.cursor()

curr.executemany(
        """
        INSERT INTO CHANGETYPE (Type, Sign)
        VALUES (%s, %s)
        ON CONFLICT (Type) DO NOTHING
        """,
            [("Purchase", "TRUE"), ("Sale","FALSE"),]
        )


curr.executemany(
        """
        INSERT INTO UNITTYPE(Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING
        """,
        [("Gram",), ("Kilogram",), ("Litre",),]
        )

conn.commit()
curr.close() 
conn.close()

