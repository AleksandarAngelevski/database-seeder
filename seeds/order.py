import os
import random
from dotenv import load_dotenv
from faker import Faker
from psycopg2.extras import execute_values

def seed_order(curr, n):
    load_dotenv()
    fake = Faker()
    curr.execute("SELECT Id FROM Employee WHERE DateResignation IS Null")
    active_employees_ids = [row[0] for row in curr.fetchall()]
    order_type_size = int(os.getenv("ORDER_TYPES_COUNT", 0))
    order_status_size = int(os.getenv("ORDER_STATUS_COUNT", 0))
    table_size = int(os.getenv("RESTAURANT_TABLE_COUNT", 0))

    batch_size = 10000
    for batch_start in range(0, n, batch_size):
        batch = []
        current_batch = min(batch_size, n - batch_start)
        for _ in range(current_batch):
            date_created = fake.date_time_between(start_date="-1y", end_date="now")
            date_finished = fake.date_time_between(start_date=date_created, end_date="now") if random.random() > 0.3 else None
            order_type = random.randint(1, order_type_size)
            table_id = None if order_type == 1 else random.randint(1, table_size)
            batch.append((
                random.choice(active_employees_ids),
                date_created,
                date_finished,
                order_type,
                random.randint(1, order_status_size),
                table_id,
            ))

        execute_values(curr, """
            INSERT INTO "Order" (WaiterId, DateCreated, DateFinished, TypeId, StatusId, TableNumber)
            VALUES %s
        """, batch)

        print(f"\rSeeding orders: {min(batch_start + batch_size, n)/n*100:.1f}%", end="", flush=True)
    print()
