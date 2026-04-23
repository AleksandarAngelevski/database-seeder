from os import wait


def seed_unit_type(curr,data=None):
    curr.executemany(
        """
        INSERT INTO UNITTYPE(Type)
        VALUES (%s)
        """
#        ON CONFLICT (Type) DO NOTHING
#        """
        ,
        [("Weight",), ("Volume",),("Count",),("Length",),]
        )


