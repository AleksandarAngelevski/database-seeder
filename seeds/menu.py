import os
import random
from dotenv import load_dotenv
from faker import Faker
from psycopg2.extras import execute_values

def seed_menu(curr):
    load_dotenv()
    fake = Faker()
    menu_size = int(os.getenv("MENU_COUNT", 0))
    menu_type_size = int(os.getenv("MENU_TYPES_COUNT", 0))
    data = [
            ('Standard Breakfast Menu', True,  1),
            ('Standard Lunch Menu',     True,  2),
            ('Standard Dinner Menu',    True,  3),
            ('Drinks Menu',             True,  4),
            ('Desserts Menu',           True,  5),
            ('Weekend Specials',        True,  6),
            ('Kids Menu',               True,  7),
            ('Winter Seasonal',         True, 8)
            ]
    execute_values(curr,"""
            INSERT INTO Menu (Name, Active, TypeId)
            VALUES %s
        """, data)


def seed_menu_item(curr):
    load_dotenv()
    product_size = int(os.getenv("PRODUCT_COUNT", 0))

    # Use a random subset of products as menu items
    product_ids = random.sample(range(1, product_size + 1), k=min(product_size, product_size))

    for i, product_id in enumerate(product_ids):
        curr.execute("""
            INSERT INTO MenuItem (Id)
            VALUES (%s)
            ON CONFLICT DO NOTHING
        """, (product_id,))
        print(f"\rSeeding menu items: {((i+1)/len(product_ids)*100):.1f}%", end="", flush=True)
    print()


