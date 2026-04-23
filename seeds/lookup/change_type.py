def seed_change_type(curr,data=None):
    curr.executemany(
        """
        INSERT INTO CHANGETYPE (Type, Sign)
        VALUES (%s, %s)
        ON CONFLICT (Type) DO NOTHING
        """,
            [("Purchase", "TRUE"), ("ORDER","FALSE"),
             ("Order","FALSE"),("Manual Adjustment Down", "FALSE")
             ,("Manual Adjustment Up","TRUE"), ("Return to Supplier","FALSE"),]
        )





