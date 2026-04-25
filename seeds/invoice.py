def seed_invoice(curr):
    curr.execute("""
        INSERT INTO Invoice (OrderId, InvoiceDate, TotalAmount, TaxAmount)
        SELECT
            o.Id,
            o.DateFinished,
            COALESCE(SUM(oi.Quantity * mm.Price), 0),
            COALESCE(ROUND(SUM(oi.Quantity * mm.Price) * 0.18, 2), 0)
        FROM "Order" o
        JOIN OrderItem oi ON oi.OrderId = o.Id
        JOIN MenuMember mm ON mm.Id = oi.MenuMemberId AND mm.MenuItemId = oi.MenuItemId
        WHERE o.StatusId = 5
        GROUP BY o.Id, o.DateFinished
    """)

    curr.execute("SELECT COUNT(*) FROM Invoice")
    print(f"Seeded {curr.fetchone()[0]} invoices")


def seed_invoice_item(curr):
    curr.execute("""
        INSERT INTO InvoiceItem (InvoiceId, OrderItemId, OriginalPrice, DiscountedPrice, Quantity)
        SELECT
            inv.Id,
            oi.Id,
            mm.Price,
            di.NewPrice,
            oi.Quantity
        FROM Invoice inv
        JOIN "Order" o ON o.Id = inv.OrderId
        JOIN OrderItem oi ON oi.OrderId = o.Id
        JOIN MenuMember mm ON mm.Id = oi.MenuMemberId AND mm.MenuItemId = oi.MenuItemId
        LEFT JOIN DiscountItem di ON di.MenuMemberId = mm.Id
                                  AND di.MenuMemberMenuItemId = mm.MenuItemId
    """)

    curr.execute("SELECT COUNT(*) FROM InvoiceItem")
    print(f"Seeded {curr.fetchone()[0]} invoice items")
