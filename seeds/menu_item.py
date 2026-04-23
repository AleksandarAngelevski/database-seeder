import os
from dotenv import load_dotenv

def seed_menu_item(curr):
    load_dotenv()
    curr.execute("""
        INSERT INTO MenuItem (Id)
        SELECT p.Id FROM Product p WHERE p.TypeId IN (2, 3, 4)
    """)
    curr.execute("SELECT COUNT(*) FROM MenuItem")
    count = curr.fetchone()[0]
    print(f"Seeded {count} menu items")
