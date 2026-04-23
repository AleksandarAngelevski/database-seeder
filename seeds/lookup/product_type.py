def seed_product_type(curr,data=None):
    curr.executemany(
        """
        INSERT INTO PRODUCTTYPE(Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING 
        """,
        [('Ingredient',), ('Beverage',), ('Dish',), ('Dessert',), ('Condiment',), ('Packaging',), ('Cleaning',)]
        )


