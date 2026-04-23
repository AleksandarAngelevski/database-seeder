def seed_menu_member(curr):
    curr.execute("""
        INSERT INTO MenuMember (MenuItemId, Price, TypeId, MenuId)
        SELECT
            mi.Id,
            CASE
                WHEN p.TypeId = 3 THEN ROUND((8 + random() * 22)::numeric, 2)
                WHEN p.TypeId = 4 THEN ROUND((3 + random() * 7)::numeric, 2)
                WHEN p.TypeId = 2 THEN ROUND((1.5 + random() * 8)::numeric, 2)
            END,
            1 + floor(random() * 4)::int,
            CASE
                WHEN p.TypeId = 3 THEN 3
                WHEN p.TypeId = 4 THEN 5
                WHEN p.TypeId = 2 THEN 4
            END
        FROM MenuItem mi
        JOIN Product p ON p.Id = mi.Id
    """)

    curr.execute("""
        INSERT INTO MenuMember (MenuItemId, Price, TypeId, MenuId)
        SELECT
            mi.Id,
            ROUND((7 + random() * 13)::numeric, 2),
            1,
            2
        FROM MenuItem mi
        JOIN Product p ON p.Id = mi.Id
        WHERE p.TypeId = 3
    """)

    curr.execute("SELECT COUNT(*) FROM MenuMember")
    count = curr.fetchone()[0]
    print(f"Seeded {count} menu members")
