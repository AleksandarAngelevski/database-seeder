import os
import random
from dotenv import load_dotenv
from faker import Faker
from psycopg2.extras import execute_values

def seed_reservation(curr):
    load_dotenv()
    fake = Faker()
    n = int(os.getenv("RESERVATIONS_COUNT", 0))
    curr.execute("SELECT MAX(TableNumber) FROM RestaurantTable")
    table_count = curr.fetchone()[0]
    curr.execute("SELECT Id FROM Employee WHERE DateResignation IS NULL")
    active_employee_ids = [row[0] for row in curr.fetchall()]

    batch_size = 10000
    inserted = 0

    while inserted < n:
        batch = []
        for _ in range(min(batch_size, n - inserted)):
            start_hour = random.randint(10, 21)
            start_min = random.choice([0, 30])
            start_time = f"{start_hour:02d}:{start_min:02d}:00"
            end_hour = start_hour + 1
            end_min = start_min + 30
            if end_min >= 60:
                end_min -= 60
                end_hour += 1
            end_time = f"{end_hour:02d}:{end_min:02d}:00"
            batch.append((
                fake.first_name() + ' ' + fake.last_name(),
                '+389 7' + str(random.randint(1000000, 9999999)),
                start_time,
                end_time,
                fake.date_between(start_date='-5y', end_date='today'),
                random.choice(active_employee_ids),
                random.randint(1, table_count),
            ))

        curr.execute("SAVEPOINT before_batch")
        try:
            execute_values(curr, """
                INSERT INTO Reservation (GuestName, GuestPhone, StartTime, EndTime, "Date", EmployeeId, TableNumber)
                VALUES %s
                ON CONFLICT DO NOTHING
            """, batch)
            # Check how many were actually inserted
            curr.execute("SELECT COUNT(*) FROM Reservation")
            total = curr.fetchone()[0]
            newly_inserted = total - inserted
            inserted = total
            if newly_inserted == 0:
                continue
        except Exception as e:
            curr.execute("ROLLBACK TO SAVEPOINT before_batch")
            continue

        print(f"\rSeeding reservations: {(inserted/n*100):.1f}%", end="", flush=True)

    print()
