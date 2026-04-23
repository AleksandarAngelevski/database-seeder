def seed_menu_type(curr, date=None):
    curr.executemany(
        """
        INSERT INTO MenuType(Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING
        """,
        [
('Breakfast',), ('Lunch',), ('Dinner',), ('Drinks',), ('Desserts',), ('Specials',), ('Kids',), ('Seasonal',),
            ])


