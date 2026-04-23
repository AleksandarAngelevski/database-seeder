import os
import random
from dotenv import load_dotenv
from psycopg2.extras import execute_values

def seed_order_item(curr):
    load_dotenv()
    employee_size = int(os.getenv("EMPLOYEE_COUNT", 0))
    order_items_per_order = int(os.getenv("ORDER_ITEMS_PER_ORDER", 5))

    curr.execute('SELECT Id FROM "Order"')
    order_ids = [row[0] for row in curr.fetchall()]

    curr.execute("SELECT Id, MenuItemId FROM MenuMember")
    menu_members = curr.fetchall()

    batch_size = 10000
    batch = []

    for i, order_id in enumerate(order_ids):
        num_items = random.randint(1, order_items_per_order)
        for _ in range(num_items):
            member_id, menu_item_id = random.choice(menu_members)
            batch.append((
                random.randint(1, order_items_per_order),  # Quantity
                order_id,                                   # OrderId
                random.randint(1, employee_size),           # CreatedBy
                random.choice([True, False]),               # Finished
                member_id,                                  # MenuMemberId
                menu_item_id,                               # MenuItemId
            ))

            if len(batch) >= batch_size:
                execute_values(curr, """
                    INSERT INTO OrderItem (Quantity, OrderId, CreatedBy, Finished, MenuMemberId, MenuItemId)
                    VALUES %s
                """, batch)
                batch = []

        print(f"\rSeeding order items: {((i+1)/len(order_ids)*100):.1f}%", end="", flush=True)

    # Insert any remaining
    if batch:
        execute_values(curr, """
            INSERT INTO OrderItem (Quantity, OrderId, CreatedBy, Finished, MenuMemberId, MenuItemId)
            VALUES %s
        """, batch)

    print()
