def seed_unit(curr):
        curr.executemany(
                """
                INSERT INTO UNIT(NAME,Conversion_to_base, TypeId)
                VALUES (%s, %s, %s)
                """,
                [
    ('gram',       1,    1),
    ('kilogram',   1000, 1),
    ('milligram',  1,    1),
    ('milliliter', 1,    2),
    ('liter',      1000, 2),
    ('centiliter', 10,   2),
    ('piece',      1,    3),
    ('dozen',      12,   3),
    ('slice',      1,    3)
                    ]
                )

