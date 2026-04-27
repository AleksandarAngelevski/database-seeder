import os
import random
from dotenv import load_dotenv
from psycopg2.extras import execute_values

import os
import random
from dotenv import load_dotenv
from psycopg2.extras import execute_values
from progress_api import get_progress, save_progress

def seed_order_item(curr, conn):
    load_dotenv()
    employee_size = int(os.getenv("EMPLOYEE_COUNT", 0))
    order_items_per_order = int(os.getenv("ORDER_ITEMS_PER_ORDER", 5))

    curr.execute('SELECT Id FROM "Order"')
    order_ids = [row[0] for row in curr.fetchall()]

    curr.execute("SELECT Id, MenuItemId FROM MenuMember")
    menu_members = curr.fetchall()

    start_from = get_progress("order_item_batch", default=0)

    batch_size = 10000
    batch = []

    for i, order_id in enumerate(order_ids):
        if i < start_from:
            continue

        num_items = random.randint(1, order_items_per_order)
        for _ in range(num_items):
            member_id, menu_item_id = random.choice(menu_members)
            batch.append((
                random.randint(1, order_items_per_order),
                order_id,
                random.randint(1, employee_size),
                random.choice([True, False]),
                member_id,
                menu_item_id,
            ))

            if len(batch) >= batch_size:
                execute_values(curr, """
                    INSERT INTO OrderItem (Quantity, OrderId, CreatedBy, Finished, MenuMemberId, MenuItemId)
                    VALUES %s
                """, batch)
                conn.commit()
                save_progress("order_item_batch", i)
                batch = []

        print(f"\rSeeding order items: {((i+1)/len(order_ids)*100):.1f}%", end="", flush=True)

    if batch:
        execute_values(curr, """
            INSERT INTO OrderItem (Quantity, OrderId, CreatedBy, Finished, MenuMemberId, MenuItemId)
            VALUES %s
        """, batch)
        conn.commit()

    save_progress("order_item_batch", len(order_ids))
    print()
