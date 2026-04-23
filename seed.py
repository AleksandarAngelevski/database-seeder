from seeds.lookup.change_type import *
from seeds.lookup.employee_type import *
from seeds.lookup.menu_member_type import *
from seeds.lookup.menu_type import *
from seeds.lookup.order_status import *
from seeds.lookup.order_type import *
from seeds.lookup.product_type import *
from seeds.lookup.table_type import *
from seeds.lookup.unit_type import *
from seeds.unit import *
from seeds.table import *
from seeds.employee import *
from seeds.employee_role import *
from seeds.product import *
from seeds.order import *
from seeds.menu import *
from seeds.menu_item import *
from seeds.menu_member import *
from seeds.order_item import *
import os
from dotenv import load_dotenv 
import psycopg2
load_dotenv()
conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        password=os.getenv("DB_PASSWORD")
#        dbname="test_advdb",
#        user="postgres",
#        host="localhost",
#        port=5432
        )

curr = conn.cursor()
TABLE_COUNT=int(os.getenv("RESTAURANT_TABLE_COUNT",0))
EMPLOYEE_COUNT=int(os.getenv("EMPLOYEE_COUNT",0))
PRODUCT_COUNT=int(os.getenv("PRODUCT_COUNT",0))
ORDERS_COUNT=int(os.getenv("ORDERS_COUNT",0))
def run_seed():
    print("CREATING MENU TYPES")
    seed_menu_type(curr)
    print("CREATING CHANGE TYPES")
    seed_change_type(curr)
    print("CREATING MENU MEMBER TYPES") 
    seed_menu_member_type(curr)
    print("CREATING ORDER STATUS") 
    seed_order_status(curr)
    print("CREATING ORDER TYPE") 
    seed_order_type(curr)
    print("CREATING PRODCUT TYPE")
    seed_product_type(curr)
    print("CREATING TABLE TYPE") 
    seed_table_type(curr) 
    print("CREATING UNIT TYPE")
    seed_unit_type(curr)
    print("CREATING UNIT")
    seed_unit(curr)
    print("CREATING RESTAURANT TABLE") 
    seed_table(curr,TABLE_COUNT)
    print("CREATING EMPLOYEE TYPES")
    seed_employee_type(curr)
    print("CREATING EMPLOYEE")
    seed_employee(curr,EMPLOYEE_COUNT)
    print("CREATING EMPLOYEE ROLES")
    seed_employee_role(curr)
    print("CREATING PRODUCTS")
    seed_product(curr,PRODUCT_COUNT)
    print("CREATING ORDERS")
    seed_order(curr,ORDERS_COUNT)
    seed_menu(curr)
    print("CREATING MENU ITEMS")
    seed_menu_item(curr)
    print("CREATING MENU MEMBERS")
    seed_menu_member(curr)
    print("CREATING ORDER ITEMS")
    seed_order_item(curr)
     

run_seed()
conn.commit()
curr.close() 
conn.close()

