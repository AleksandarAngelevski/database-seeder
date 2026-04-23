import os
import random
from dotenv import load_dotenv
from faker import Faker

def seed_product(curr,n):
    load_dotenv()
    fake = Faker()
    product_type_size = int(os.getenv("PRODUCT_TYPES_COUNT", 0))
    unit_size = int(os.getenv("UNIT_TYPES_COUNT", 0))

    for i in range(n):
        data = (
            fake.unique.word().capitalize(),  # Name
            fake.image_url(),                 # Url
            random.randint(1, product_type_size),  # TypeId
            random.randint(1, unit_size),          # BaseUnitId
        )
        curr.execute("""
            INSERT INTO PRODUCT (Name, Url, TypeId, BaseUnitId)
            VALUES (%s, %s, %s, %s)
        """, data)
        print(f"\rSeeding products: {((i+1)/n*100):.1f}%", end="", flush=True)
    print()



data = [
        ('Wheat Flour',1,1),('Sugar',1,1),('Salt',1,1),('Butter',1,1),
    ('Olive Oil',1,4),('Sunflower Oil',1,4),('Milk',1,4),('Eggs',1,7),
    ('Chicken Breast',1,1),('Beef Mince',1,1),('Pork Ribs',1,1),
    ('Salmon Fillet',1,1),('Tuna',1,1),('Shrimp',1,1),
    ('Tomatoes',1,1),('Onions',1,1),('Garlic',1,1),('Bell Pepper',1,1),
    ('Mushrooms',1,1),('Spinach',1,1),('Lettuce',1,1),('Cucumber',1,1),
    ('Potatoes',1,1),('Carrots',1,1),('Cheese',1,1),('Mozzarella',1,1),
    ('Parmesan',1,1),('Cream',1,4),('Tomato Sauce',1,4),('Pasta',1,1),
    ('Rice',1,1),('Bread',1,7),('Bun',1,7),('Bacon',1,1),('Ham',1,1),
    ('Lemon',1,7),('Basil',1,1),('Black Pepper',1,1),('Paprika',1,1),
    ('Cocoa Powder',1,1),('Chocolate',1,1),('Honey',1,4),('Yeast',1,1),
    ('Espresso',2,4),('Americano',2,4),('Cappuccino',2,4),('Latte',2,4),
    ('Green Tea',2,4),('Black Tea',2,4),('Orange Juice',2,4),('Apple Juice',2,4),
    ('Still Water',2,4),('Sparkling Water',2,4),('Coca-Cola',2,4),('Sprite',2,4),
    ('Fanta',2,4),('Beer Domestic',2,4),('Beer Imported',2,4),
    ('Red Wine Glass',2,4),('White Wine Glass',2,4),('House Wine Bottle',2,4),           ('Prosecco',2,4),('Lemonade',2,4), ('Margherita Pizza',3,7),('Pepperoni Pizza',3,7),('BBQ Chicken Pizza',3,7), ('Veggie Pizza',3,7),('Spaghetti Bolognese',3,7),('Spaghetti Carbonara',3,7), ('Penne Arrabbiata',3,7),('Lasagna',3,7),('Chicken Burger',3,7),
    ('Beef Burger',3,7),('Veggie Burger',3,7),('Club Sandwich',3,7),
    ('Caesar Salad',3,7),('Greek Salad',3,7),('Mixed Grill',3,7),
    ('Grilled Salmon',3,7),('Shrimp Pasta',3,7),('Chicken Wings',3,7),
    ('Nachos',3,7),('French Fries',3,7),('Onion Rings',3,7),
    ('Soup of the Day',3,7),('Bruschetta',3,7),('Garlic Bread',3,7),
    ('Steak Medium',3,7),('Steak Well Done',3,7),('Fish and Chips',3,7),
    ('Chicken Schnitzel',3,7),('Mushroom Risotto',3,7),('Vegetable Stir Fry',3,7),
        ('Tiramisu',4,7),('Cheesecake',4,7),('Chocolate Cake',4,7),
    ('Ice Cream Scoop',4,7),('Crepes',4,7),('Panna Cotta',4,7),
    ('Baklava',4,7),('Fruit Salad',4,7)
        ]
