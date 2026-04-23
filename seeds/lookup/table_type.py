def seed_table_type(curr, data=None):
    curr.executemany(
        """
        INSERT INTO TABLETYPE (Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING
        """,
        [('Indoor',), ('Outdoor',), ('Bar',), ('Private Room',), ('Terrace',)]
        )
