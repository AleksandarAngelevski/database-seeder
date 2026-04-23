def seed_order_type(curr, data=None): 
    curr.executemany(
        """
        INSERT INTO ORDERTYPE(Type)
        VALUES (%s)
        ON CONFLICT (Type) DO NOTHING
        """,[("Takeaway",), ("Dine-in",),("Delivery",), ("Bar",)]
            )
