def seed_stored_product(curr):
    curr.execute("""
        INSERT INTO StoredProduct (Quantity, ProductId)
        SELECT
            CASE
                WHEN TypeId = 1 THEN floor(50000 + random() * 100000)::int
                WHEN TypeId = 2 THEN floor(500   + random() * 2000)::int
                ELSE 0
            END,
            Id
        FROM Product
    """)

    curr.execute("SELECT COUNT(*) FROM StoredProduct")
    count = curr.fetchone()[0]
    print(f"Seeded {count} stored products")
