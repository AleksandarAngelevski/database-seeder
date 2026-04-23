def seed_order_status(curr,data=None):
    curr.executemany(
    """
    INSERT INTO ORDERSTATUS(Status)
    Values (%s)
    ON CONFLICT (Status) DO NOTHING
    """,
    [("PENDING",), ("FINISHED",), ("CANCELLED",)]
        )


