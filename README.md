## Requirements

- Python 3.10+
- PostgreSQL
- SSH tunnel for access to a remote database server 
## Installation

```bash
git clone https://github.com/AleksandarAngelevski/database-seeder
cd database-seeder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy the `.env.example` file and fill in your database credentials:

```env

# Database
DB_HOST=localhost
DB_PORT=5433
DB_NAME=your-database-name
DB_USER=your-db-username
DB_PASSWORD=your-db-password

# Seed counts
EMPLOYEE_COUNT=50
EMPLOYEE_TYPES_COUNT=5
PRODUCT_COUNT=100
PRODUCT_TYPES_COUNT=4
TABLE_COUNT=40
TABLE_TYPES_COUNT=3
UNIT_TYPES_COUNT=3
ORDERS_COUNT=1000000
ORDER_ITEMS_PER_ORDER=5
ORDER_TYPES_COUNT=3
ORDER_STATUS_COUNT=5
RESERVATIONS_COUNT=200000
MENU_COUNT=8
MENU_TYPES_COUNT=8
MENU_MEMBER_TYPES_COUNT=4
DISCOUNT_COUNT=20
```

## Usage

**1. Set up the schema:**
```bash
psql -h localhost -p 5433 -U your-db-user -d your-db-name -f schema.sql
```

**2. Create views:**
```bash
psql -h localhost -p 5433 -U your-db-user -d your-db-name -f views.sql
```

**3. Run the seeder:**
```bash
python -m seed
```

If the script fails mid-way, re-run it — completed steps will be skipped automatically via `seed_progress.json`.

**4. To reset and reseed from scratch:**
```bash
rm seed_progress.json
psql -h localhost -p 5433 -U your-db-user -d your-db-name -f drop.sql
psql -h localhost -p 5433 -U your-db-user -d your-db-name -f schema.sql
python -m seed
```

## Features

- Batch inserts using `execute_values` for performance
- Progress tracking with `seed_progress.json` — resume from last successful batch on failure
- Realistic data generation with Faker
- Triggers enforced at DB level:
  - Resigned employees cannot create orders
  - No overlapping table reservations
  - Order must have all items finished before marking as complete
- SSH tunnel support for remote university DB server

## Database Schema

The schema includes the following tables:

`EmployeeType` `Employee` `EmployeeRole` `OrderType` `OrderStatus` `MenuType` `ProductType` `MenuMemberType` `TableType` `UnitType` `Unit` `RestaurantTable` `Product` `MenuItem` `StoredProduct` `ConsistsOf` `Menu` `MenuMember` `Discount` `DiscountItem` `Order` `OrderItem` `Reservation` `Invoice` `InvoiceItem` `ProductUsageLog` `Location` `ChangeType`
