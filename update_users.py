from faker import Faker
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_batch
import os

load_dotenv()

fake = Faker()
conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD")
#        dbname="test_advdb",
#        user="postgres",
#        host="localhost",
#        port=5432
        )
curr = conn.cursor()

curr.execute(
        """
        SELECT id, sex FROM EMPLOYEE;
        """
        )

rows = curr.fetchall()
rows = [list(_) for _ in rows]
new_rows = []
for _ in rows:
    if _[1] == 'F':
        _.append(fake.first_name_female())
        _.append(fake.last_name_female())
    else:
        _.append(fake.first_name_male())
        _.append(fake.last_name_male())
    _ = [_[2], _[3], _[0]]
    new_rows.append(_)


query = """
UPDATE Employee
SET 
firstname = %s,
lastname = %s
WHERE id = %s
"""


execute_batch(curr, query, new_rows)

conn.commit()


