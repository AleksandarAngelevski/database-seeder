from faker import Faker 
import random
import os
from dotenv import load_dotenv
def seed_table(curr, n=1):
    load_dotenv()
    fake = Faker()
    for _ in range(n):
        data = (random.randint(2,7), random.randint(1,int(os.getenv("TABLE_TYPES_COUNT"))))
        curr.execute(
                """
                INSERT INTO RESTAURANTTABLE (CAPACITY, TABLETYPEID)
                VALUES(%s, %s)
                """,
                data
                )
        print(f"\rSeeding tables: {((_+1)/n*100):.1f}%",end="", flush=True)
    print()
