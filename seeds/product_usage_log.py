import os
import random
from dotenv import load_dotenv
from faker import Faker
from psycopg2.extras import execute_values
from datetime import timedelta

def seed_product_usage_log(curr, weeks=312, monthly_months=71, order_sample_limit=2500000):
    load_dotenv()

    # Weekly restocks
    curr.execute("""
        INSERT INTO ProductUsageLog (ProductId, ChangeAmount, InputAmount, Timestamp, ChangeTypeId, BaseUnitId, InputUnitId)
        SELECT
            p.Id,
            floor(5000 + random() * 15000)::int,
            floor(5 + random() * 15)::int,
            ('2019-01-01'::timestamp + (week_n * interval '1 week') + (random() * interval '5 days')),
            1,
            p.BaseUnitId,
            CASE WHEN p.BaseUnitId = 1 THEN 2 WHEN p.BaseUnitId = 4 THEN 5 ELSE p.BaseUnitId END
        FROM Product p
        CROSS JOIN generate_series(0, %s) AS week_n
        WHERE p.TypeId = 1
    """, (weeks,))
    curr.execute("SELECT COUNT(*) FROM ProductUsageLog")
    print(f"Seeded {curr.fetchone()[0]} restock logs")

    # Daily usage sampled from orders
    curr.execute("""
        INSERT INTO ProductUsageLog (ProductId, ChangeAmount, InputAmount, Timestamp, ChangeTypeId, BaseUnitId, InputUnitId)
        SELECT
            p.Id,
            floor(50 + random() * 500)::int,
            floor(50 + random() * 500)::int,
            o.DateCreated,
            2,
            p.BaseUnitId,
            p.BaseUnitId
        FROM "Order" o
        CROSS JOIN LATERAL (
            SELECT Id, BaseUnitId FROM Product
            WHERE TypeId = 1
            ORDER BY random()
            LIMIT 3
        ) p
        WHERE o.Id %% 10 = 0
        LIMIT %s
    """, (order_sample_limit,))
    curr.execute("SELECT COUNT(*) FROM ProductUsageLog")
    print(f"Seeded {curr.fetchone()[0]} usage logs")

    # Monthly waste/spoilage
    curr.execute("""
        INSERT INTO ProductUsageLog (ProductId, ChangeAmount, InputAmount, Timestamp, ChangeTypeId, BaseUnitId, InputUnitId)
        SELECT
            p.Id,
            floor(100 + random() * 1000)::int,
            floor(100 + random() * 1000)::int,
            ('2019-01-01'::date + (month_n * interval '1 month') + (random() * interval '28 days'))::timestamp,
            3,
            p.BaseUnitId,
            p.BaseUnitId
        FROM Product p
        CROSS JOIN generate_series(0, %s) AS month_n
        WHERE p.TypeId = 1
    """, (monthly_months,))
    curr.execute("SELECT COUNT(*) FROM ProductUsageLog")
    print(f"Seeded {curr.fetchone()[0]} total usage logs")
