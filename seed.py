from seeds.invoice import seed_invoice
from seeds.lookup.change_type import *
from seeds.lookup.employee_type import *
from seeds.lookup.menu_member_type import *
from seeds.lookup.menu_type import *
from seeds.lookup.order_status import *
from seeds.lookup.order_type import *
from seeds.lookup.product_type import *
from seeds.lookup.table_type import *
from seeds.lookup.unit_type import *
from seeds.reservation import seed_reservation
from seeds.stored_product import *
from seeds.recipe import *
from seeds.product_usage_log import *
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
from seeds.discount import *
from seeds.invoice import *
from datetime import datetime
import os
from dotenv import load_dotenv 
import psycopg2
from progress_api import *


start = datetime.now()
print(f"Start at: {start.strftime('%H:%M:%S')}")
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


def run_step(name, fn, *args, needs_con=False):
    if is_done(name):
        print(f"SKIPPING {name} (already done)")
        return
    print(f"CREATING {name}")
    if needs_con:
        fn(curr, conn,*args)
    else:
        fn(curr, *args)
    conn.commit()
    save_progress(name, True)

def run_seed():
    run_step("MENU TYPES",        seed_menu_type)
    run_step("CHANGE TYPES",      seed_change_type)
    run_step("MENU MEMBER TYPES", seed_menu_member_type)
    run_step("ORDER STATUS",      seed_order_status)
    run_step("ORDER TYPE",        seed_order_type)
    run_step("PRODUCT TYPE",      seed_product_type)
    run_step("TABLE TYPE",        seed_table_type)
    run_step("UNIT TYPE",         seed_unit_type)
    run_step("UNIT",              seed_unit)
    run_step("RESTAURANT TABLE",  seed_table,          TABLE_COUNT)
    run_step("EMPLOYEE TYPES",    seed_employee_type)
    run_step("EMPLOYEE",          seed_employee,       EMPLOYEE_COUNT)
    run_step("EMPLOYEE ROLES",    seed_employee_role)
    run_step("PRODUCTS",          seed_product)
    run_step("ORDERS",            seed_order,          ORDERS_COUNT)
    run_step("MENU",              seed_menu)
    run_step("MENU ITEMS",        seed_menu_item)
    run_step("MENU MEMBERS",      seed_menu_member)
    run_step("ORDER ITEMS",       seed_order_item, needs_con=True)
    run_step("DISCOUNTS",         seed_discount)
    run_step("RECIPES",           seed_consists_of)
    run_step("STORED PRODUCTS",   seed_stored_product)
    run_step("RESERVATIONS",      seed_reservation, needs_con=True)
    run_step("INVOICE", seed_invoice)
    run_step("INVOICE ITEM", seed_invoice_item)
    run_step("PRODUCT USAGE LOGS",seed_product_usage_log)



run_seed()
conn.commit()
curr.close() 
conn.close()

end = datetime.now()
elapsed = end - start
print(f"Finished at: {end.strftime('%H:%M:%S')}")
print(f"Total time: {str(elapsed).split('.')[0]}")















generate= """
CREATE TABLE EmployeeType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(30) NOT NULL UNIQUE,
    Permissions INT4 NOT NULL DEFAULT 0
);

CREATE TABLE OrderType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE OrderStatus (
    Id SERIAL PRIMARY KEY,
    Status VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE MenuType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE ProductType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE MenuMemberType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE TableType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE UnitType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE ChangeType (
    Id SERIAL PRIMARY KEY,
    Type VARCHAR(30) NOT NULL UNIQUE,
    Sign BOOL NOT NULL
);

CREATE TABLE Location (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL UNIQUE
);

-- Core Tables

CREATE TABLE Unit (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(20) NOT NULL,
    Conversion_to_base INT4 NOT NULL DEFAULT 1 CHECK (Conversion_to_base > 0),
    TypeId INT4 NOT NULL,
    CONSTRAINT FKUnit_UnitType FOREIGN KEY (TypeId) REFERENCES UnitType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE RestaurantTable (
    TableNumber SERIAL PRIMARY KEY,
    Capacity INT4 NOT NULL DEFAULT 2 CHECK (Capacity > 0),
    Status BOOL NOT NULL DEFAULT TRUE,
    TableTypeId INT4 NOT NULL,
    CONSTRAINT FKTable_TableType FOREIGN KEY (TableTypeId) REFERENCES TableType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Employee (
    Id SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL DEFAULT 'Unknown',
    LastName VARCHAR(50) NOT NULL DEFAULT 'Unknown',
    SSN VARCHAR(13) NOT NULL UNIQUE,
    Sex CHAR(1) NOT NULL CHECK (Sex IN ('M', 'F', 'O')),
    Email VARCHAR(100) UNIQUE CHECK (Email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$'),
    PasswordHash VARCHAR(255) NOT NULL,
    DateEmployment DATE NOT NULL DEFAULT CURRENT_DATE,
    DateResignation DATE,
    CHECK (DateResignation IS NULL OR DateResignation >= DateEmployment)
);

CREATE TABLE EmployeeRole (
    Id SERIAL PRIMARY KEY,
    EmployeeId INT4 NOT NULL,
    EmployeeTypeid INT4 NOT NULL,
    CONSTRAINT FKEmployeeRole_Employee FOREIGN KEY (EmployeeId) REFERENCES Employee (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKEmployeeRole_EmployeeType FOREIGN KEY (EmployeeTypeid) REFERENCES EmployeeType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Product (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL UNIQUE,
    Url VARCHAR(255),
    TypeId INT4 NOT NULL,
    BaseUnitId INT4 NOT NULL,
    CONSTRAINT FKProduct_ProductType FOREIGN KEY (TypeId) REFERENCES ProductType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKProduct_Unit FOREIGN KEY (BaseUnitId) REFERENCES Unit (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE MenuItem (
    Id INT4 PRIMARY KEY,
    CONSTRAINT FKMenuItem_Product FOREIGN KEY (Id) REFERENCES Product (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE StoredProduct (
    Id SERIAL PRIMARY KEY,
    Quantity INT4 NOT NULL DEFAULT 0 CHECK (Quantity >= 0),
    ProductId INT4 NOT NULL,
    CONSTRAINT FKStoredProduct_Product FOREIGN KEY (ProductId) REFERENCES Product (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE ConsistsOf (
    Parent INT4 NOT NULL,    -- The Recipe
    Component INT4 NOT NULL, -- The Ingredient
    Amount INT4 NOT NULL CHECK (Amount > 0),
    UnitId INT4 NOT NULL,
    PRIMARY KEY (Parent, Component),
    CONSTRAINT FKConsistsOf_ParentProduct FOREIGN KEY (Parent) REFERENCES Product (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKConsistsOf_ComponentProduct FOREIGN KEY (Component) REFERENCES Product (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKConsistsOf_Unit FOREIGN KEY (UnitId) REFERENCES Unit (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE ProductUsageLog (
    Id SERIAL PRIMARY KEY,
    ProductId INT4 NOT NULL,
    ChangeAmount INT4 NOT NULL,
    InputAmount INT4 NOT NULL,
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ChangeTypeId INT4 NOT NULL,
    BaseUnitId INT4 NOT NULL,
    InputUnitId INT4 NOT NULL,
    CONSTRAINT FKProductUsageLog_Product FOREIGN KEY (ProductId) REFERENCES Product (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKProductUsageLog_ChangeType FOREIGN KEY (ChangeTypeId) REFERENCES ChangeType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKProductUsageLog_BaseUnit FOREIGN KEY (BaseUnitId) REFERENCES Unit (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKProductUsageLog_InputUnit FOREIGN KEY (InputUnitId) REFERENCES Unit (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Menu (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL DEFAULT 'Standard Menu',
    Active BOOL NOT NULL DEFAULT TRUE,
    Wallpaper VARCHAR(255),
    TypeId INT4 NOT NULL,
    CONSTRAINT FKMenu_MenuType FOREIGN KEY (TypeId) REFERENCES MenuType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE MenuMember (
    Id SERIAL NOT NULL,
    MenuItemId INT4 NOT NULL,
    Price NUMERIC(10,2) NOT NULL CHECK (Price >= 0),
    TypeId INT4 NOT NULL,
    MenuId INT4 NOT NULL,
    PRIMARY KEY (Id, MenuItemId),
    CONSTRAINT FKMenuMember_MenuItem FOREIGN KEY (MenuItemId) REFERENCES MenuItem (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKMenuMember_MenuMemberType FOREIGN KEY (TypeId) REFERENCES MenuMemberType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKMenuMember_Menu FOREIGN KEY (MenuId) REFERENCES Menu (Id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Discount (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    "From" DATE NOT NULL,
    "To" DATE NOT NULL,
    MenuId INT4 NOT NULL,
    Status BOOL NOT NULL DEFAULT TRUE,
    CONSTRAINT FKDiscount_Menu FOREIGN KEY (MenuId) REFERENCES Menu (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK ("To" >= "From")
);

CREATE TABLE DiscountItem (
    Id SERIAL PRIMARY KEY,
    NewPrice NUMERIC(10,2) NOT NULL CHECK (NewPrice >= 0),
    MenuMemberId INT4 NOT NULL,
    MenuMemberMenuItemId INT4 NOT NULL,
    DiscountId INT4 NOT NULL,
    CONSTRAINT FKDiscountItem_Discount FOREIGN KEY (DiscountId) REFERENCES Discount (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKDiscountItem_MenuMember FOREIGN KEY (MenuMemberId, MenuMemberMenuItemId) REFERENCES MenuMember (Id, MenuItemId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE "Order" (
    Id SERIAL PRIMARY KEY,
    WaiterId INT4,
    DateCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    DateFinished TIMESTAMP,
    TypeId INT4 NOT NULL,
    StatusId INT4 NOT NULL,
    TableNumber INT4,
    CONSTRAINT FKOrder_OrderType FOREIGN KEY (TypeId) REFERENCES OrderType (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKOrder_OrderStatus FOREIGN KEY (StatusId) REFERENCES OrderStatus (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FKOrder_Employee FOREIGN KEY (WaiterId) REFERENCES Employee (Id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT FKOrder_Table FOREIGN KEY (TableNumber) REFERENCES RestaurantTable (TableNumber)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE OrderItem (
    Id SERIAL PRIMARY KEY,
    Quantity INT4 NOT NULL CHECK (Quantity > 0),
    OrderId INT4 NOT NULL,
    CreatedBy INT4,
    Finished BOOL NOT NULL DEFAULT FALSE,
    MenuMemberId INT4 NOT NULL,
    MenuItemId INT4 NOT NULL,
    CONSTRAINT FKOrderItem_Order FOREIGN KEY (OrderId) REFERENCES "Order" (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKOrderItem_Employee FOREIGN KEY (CreatedBy) REFERENCES Employee (Id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT FKOrderItem_MenuMember FOREIGN KEY (MenuMemberId, MenuItemId) REFERENCES MenuMember (Id, MenuItemId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Reservation (
    Id SERIAL PRIMARY KEY,
    GuestName VARCHAR(20) NOT NULL,
    GuestPhone VARCHAR(20),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    "Date" DATE NOT NULL,
    EmployeeId INT4,
    TableNumber INT4,
    CONSTRAINT FKReservation_Employee FOREIGN KEY (EmployeeId) REFERENCES Employee (Id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT FKReservation_Table FOREIGN KEY (TableNumber) REFERENCES RestaurantTable (TableNumber)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CHECK (EndTime > StartTime)
);

CREATE TABLE Invoice (
    Id SERIAL PRIMARY KEY,
    OrderId INT4 NOT NULL,
    InvoiceDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (TotalAmount >= 0),
    TaxAmount NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (TaxAmount >= 0),
    CONSTRAINT FKInvoice_Order FOREIGN KEY (OrderId) REFERENCES "Order" (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE InvoiceItem (
    Id SERIAL PRIMARY KEY,
    InvoiceId INT4 NOT NULL,
    OrderItemId INT4 NOT NULL,
    OriginalPrice NUMERIC(10,2) NOT NULL CHECK (OriginalPrice >= 0),
    DiscountedPrice NUMERIC(10,2) CHECK (DiscountedPrice >= 0),
    Quantity INT4 NOT NULL CHECK (Quantity > 0),
    CONSTRAINT FKInvoiceItem_Invoice FOREIGN KEY (InvoiceId) REFERENCES Invoice (Id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FKInvoiceItem_OrderItem FOREIGN KEY (OrderItemId) REFERENCES OrderItem (Id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- 1. Full Order Overview
CREATE VIEW vw_order_overview AS
SELECT 
    o.Id AS OrderId,
    e.FirstName || ' ' || e.LastName AS Waiter,
    rt.TableNumber,
    rt.Capacity,
    ot.Type AS OrderType,
    os.Status AS OrderStatus,
    o.DateCreated,
    o.DateFinished
FROM "Order" o
LEFT JOIN Employee e ON o.WaiterId = e.Id
LEFT JOIN RestaurantTable rt ON o.TableNumber = rt.TableNumber
JOIN OrderType ot ON o.TypeId = ot.Id
JOIN OrderStatus os ON o.StatusId = os.Id;


-- 2. Order Items with Product and Price Info
CREATE VIEW vw_order_items_detail AS
SELECT
    oi.OrderId,
    p.Name AS Product,
    oi.Quantity,
    mm.Price AS UnitPrice,
    oi.Quantity * mm.Price AS TotalPrice,
    oi.Finished,
    e.FirstName || ' ' || e.LastName AS PreparedBy
FROM OrderItem oi
JOIN MenuMember mm ON oi.MenuMemberId = mm.Id AND oi.MenuItemId = mm.MenuItemId
JOIN MenuItem mi ON mm.MenuItemId = mi.Id
JOIN Product p ON mi.Id = p.Id
LEFT JOIN Employee e ON oi.CreatedBy = e.Id;


-- 3. Invoice Summary
CREATE VIEW vw_invoice_summary AS
SELECT
    i.Id AS InvoiceId,
    o.Id AS OrderId,
    e.FirstName || ' ' || e.LastName AS Waiter,
    i.InvoiceDate,
    i.TotalAmount,
    i.TaxAmount,
    i.TotalAmount - i.TaxAmount AS NetAmount
FROM Invoice i
JOIN "Order" o ON i.OrderId = o.Id
LEFT JOIN Employee e ON o.WaiterId = e.Id;


-- 4. Active Menu with Items and Prices
CREATE VIEW vw_active_menu AS
SELECT
    m.Name AS Menu,
    mt.Type AS MenuType,
    p.Name AS Product,
    mm.Price,
    mmt.Type AS MemberType
FROM Menu m
JOIN MenuType mt ON m.TypeId = mt.Id
JOIN MenuMember mm ON mm.MenuId = m.Id
JOIN MenuItem mi ON mm.MenuItemId = mi.Id
JOIN Product p ON mi.Id = p.Id
JOIN MenuMemberType mmt ON mm.TypeId = mmt.Id
WHERE m.Active = TRUE;


-- 5. Employee Overview with Roles
CREATE VIEW vw_employee_roles AS
SELECT
    e.Id AS EmployeeId,
    e.FirstName || ' ' || e.LastName AS FullName,
    e.SSN,
    e.Sex,
    e.Email,
    e.DateEmployment,
    e.DateResignation,
    et.Type AS Role,
    et.Permissions
FROM Employee e
JOIN EmployeeRole er ON e.Id = er.EmployeeId
JOIN EmployeeType et ON er.EmployeeTypeid = et.Id;


-- 6. Table Availability
CREATE VIEW vw_table_availability AS
SELECT
    rt.TableNumber,
    rt.Capacity,
    tt.Type AS TableType,
    rt.Status AS Available
FROM RestaurantTable rt
JOIN TableType tt ON rt.TableTypeId = tt.Id;


-- 7. Product Inventory
CREATE VIEW vw_inventory AS
SELECT
    p.Name AS Product,
    pt.Type AS ProductType,
    sp.Quantity,
    u.Name AS BaseUnit
FROM StoredProduct sp
JOIN Product p ON sp.ProductId = p.Id
JOIN ProductType pt ON p.TypeId = pt.Id
JOIN Unit u ON p.BaseUnitId = u.Id;


-- 9. Reservations Overview
CREATE VIEW vw_reservations AS
SELECT
    r.Id AS ReservationId,
    r.GuestName,
    r.GuestPhone,
    r."Date",
    r.StartTime,
    r.EndTime,
    rt.TableNumber,
    rt.Capacity,
    e.FirstName || ' ' || e.LastName AS HandledBy
FROM Reservation r
LEFT JOIN RestaurantTable rt ON r.TableNumber = rt.TableNumber
LEFT JOIN Employee e ON r.EmployeeId = e.Id;


-- 10. Revenue per Waiter
CREATE VIEW vw_revenue_per_waiter AS
SELECT
    e.FirstName || ' ' || e.LastName AS Waiter,
    COUNT(DISTINCT o.Id) AS TotalOrders,
    SUM(i.TotalAmount) AS TotalRevenue,
    AVG(i.TotalAmount) AS AvgOrderValue
FROM "Order" o
JOIN Employee e ON o.WaiterId = e.Id
JOIN Invoice i ON i.OrderId = o.Id
GROUP BY e.Id, e.FirstName, e.LastName;







-- Constraints

CREATE OR REPLACE FUNCTION check_waiter_active()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.WaiterId IS NOT NULL THEN
        IF EXISTS (
            SELECT 1 FROM Employee
            WHERE Id = NEW.WaiterId
            AND DateResignation IS NOT NULL
            AND DateResignation < NEW.DateCreated
        ) THEN
            RAISE EXCEPTION 'Waiter % has resigned and cannot create orders', NEW.WaiterId;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_waiter_active
BEFORE INSERT OR UPDATE ON "Order"
FOR EACH ROW EXECUTE FUNCTION check_waiter_active();


"""
