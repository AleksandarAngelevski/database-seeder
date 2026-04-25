
def seed_consists_of(curr):
    recipes = [
        ('Margherita Pizza',    ['Wheat Flour','Tomato Sauce','Mozzarella','Basil','Olive Oil','Salt']),
        ('Spaghetti Bolognese', ['Pasta','Beef Mince','Tomato Sauce','Onions','Garlic','Black Pepper']),
        ('Caesar Salad',        ['Lettuce','Parmesan','Garlic']),
        ('Beef Burger',         ['Beef Mince','Bun','Lettuce','Tomatoes','Cheese']),
        ('Tiramisu',            ['Eggs','Sugar','Cocoa Powder','Cream','Chocolate']),
    ]

    for dish, ingredients in recipes:
        curr.execute("""
            INSERT INTO ConsistsOf (Parent, Component, Amount, UnitId)
            SELECT dish.Id, p.Id, floor(10 + random() * 200)::int, 1
            FROM (SELECT Id FROM Product WHERE Name = %s) dish,
                 (SELECT Id FROM Product WHERE Name = ANY(%s)) p
        """, (dish, ingredients))

    curr.execute("SELECT COUNT(*) FROM ConsistsOf")
    count = curr.fetchone()[0]
    print(f"Seeded {count} recipe components")
