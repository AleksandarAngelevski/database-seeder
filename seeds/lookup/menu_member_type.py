def seed_menu_member_type(curr,data=None):
    curr.executemany(
        """
        INSERT INTO MENUMEMBERTYPE(Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING
        """,
        [('Regular',), ('Special',), ('Seasonal',), ('Chef''s Pick',)]
        )


