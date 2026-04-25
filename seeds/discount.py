import os
import random
from dotenv import load_dotenv
from faker import Faker
from psycopg2.extras import execute_values


def seed_discount(curr):
    load_dotenv()
    fake = Faker()

    curr.execute("SELECT COUNT(*) FROM Menu")
    menu_count = curr.fetchone()[0]
    DISCOUNT_COUNT= int(os.getenv("DISCOUNTS_COUNT",0))
    discounts = []
    for _ in range(DISCOUNT_COUNT):
        start_date = fake.date_between(start_date='-2y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+1y')
        discounts.append((
            fake.word().capitalize() + ' ' + random.choice(['Deal', 'Special', 'Offer', 'Discount', 'Promo']),
            start_date,
            end_date,
            random.randint(1, menu_count),
            random.choice([True, False]),
        ))

    execute_values(curr, """
        INSERT INTO Discount (Name, "From", "To", MenuId, Status)
        VALUES %s
    """, discounts)

    curr.execute("SELECT COUNT(*) FROM Discount")
    discount_count = curr.fetchone()[0]

    curr.execute("""
        INSERT INTO DiscountItem (NewPrice, MenuMemberId, MenuMemberMenuItemId, DiscountId)
        SELECT
            ROUND((mm.Price * (0.6 + random() * 0.25))::numeric, 2),
            mm.Id,
            mm.MenuItemId,
            (1 + floor(random() * %s))::int
        FROM MenuMember mm
        ORDER BY random()
        LIMIT %s
    """, (discount_count, DISCOUNT_COUNT * 5))


    curr.execute("SELECT COUNT(*) FROM DiscountItem")
    count = curr.fetchone()[0]
    print(f"Seeded {DISCOUNT_COUNT} discounts and {count} discount items")
