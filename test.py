from models import *
from seeds.employee import seed_employee
import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()
conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD")
        )

curr = conn.cursor()

seed_employee(curr,10)

conn.commit()
curr.close() 
conn.close()

