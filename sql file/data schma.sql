create database DA_Hackathon;
use DA_Hackathon;



-- Dark Store Down :: schema (MySQL / Postgres compatible)
-- Messy tables load every column as text on purpose: cleaning is part of the task.

DROP TABLE IF EXISTS orders_clean;
CREATE TABLE orders_clean (
  order_id TEXT,
  store_id TEXT,
  customer_id TEXT,
  order_ts TEXT,
  delivered_ts TEXT,
  promised_minutes INTEGER,
  order_status TEXT,
  promo_code TEXT,
  gross_amount REAL,
  discount_amount REAL,
  net_amount REAL,
  cogs_amount REAL,
  delivery_cost REAL,
  delivery_partner_id TEXT
);
-- LOAD DATA LOCAL INFILE '"D:\Accio Job Data analysis\da hackathon project\New folder\orders_clean.csv"' INTO TABLE orders_clean FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/orders_clean.csv' 
INTO TABLE orders_clean 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE IF EXISTS dark_stores_messy;
CREATE TABLE dark_stores (
  store_id VARCHAR(255),
  store_name VARCHAR(255),
  pincode VARCHAR(255),
  opened_date VARCHAR(255),
  sqft VARCHAR(255),
  monthly_rent VARCHAR(255),
  staff_count VARCHAR(255),
  cold_storage_capacity VARCHAR(255),
  city VARCHAR(255)
);
-- LOAD DATA LOCAL INFILE "D:\Accio Job Data analysis\da hackathon project\New folder\Dark_Stores.csv" INTO TABLE dark_stores FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/Dark_Stores.csv' 
INTO TABLE dark_stores 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE IF EXISTS store_hours;
CREATE TABLE store_hours (
  store_id VARCHAR(255),
  day_of_week VARCHAR(255),
  open_time VARCHAR(255),
  close_time VARCHAR(255)
);
 -- LOAD DATA LOCAL INFILE "D:\Accio Job Data analysis\da hackathon project\New folder\Store_Hours.csv" INTO TABLE store_hours FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/Store_Hours.csv' 
INTO TABLE store_hours 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE IF EXISTS delivery_partners;
CREATE TABLE delivery_partners (
  partner_id VARCHAR(255),
  partner_name VARCHAR(255),
  joined_date VARCHAR(255),
  vehicle_type VARCHAR(255),
  home_store_id VARCHAR(255),
  employment_type VARCHAR(255),
  rating VARCHAR(255)
);
 -- LOAD DATA LOCAL INFILE "D:\Accio Job Data analysis\da hackathon project\New folder\Delivery_Partners.csv" INTO TABLE delivery_partners FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/Delivery_Partners.csv' 
INTO TABLE delivery_partners 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE IF EXISTS trip_logs_messy;
CREATE TABLE trip_logs (
  trip_id VARCHAR(255),
  order_id VARCHAR(255),
  partner_id VARCHAR(255),
  picked_ts VARCHAR(255),
  delivered_ts VARCHAR(255),
  distance_km VARCHAR(255),
  trip_status VARCHAR(255)
);
-- LOAD DATA LOCAL INFILE 'D:\Accio Job Data analysis\da hackathon project\New folder\Trip_Logs.csv' INTO TABLE trip_logs FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/Trip_Logs.csv' 
INTO TABLE trip_logs 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

select * from trip_logs;

DROP TABLE IF EXISTS order_items;

CREATE TABLE order_items (
    order_item_id VARCHAR(255),
    order_id      VARCHAR(255),
    sku           VARCHAR(255),
    unit_price    DECIMAL(10,2),
    unit_cost     DECIMAL(10,2),
    quantity      INT
);
 -- LOAD DATA LOCAL INFILE "D:/Accio Job Data analysis/da hackathon project/New folder/Order_Item.csv" INTO TABLE order_items FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;


LOAD DATA LOCAL INFILE 'D:/Accio Job Data analysis/da hackathon project/New folder/Order_Item.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(order_item_id, order_id, sku, unit_price, unit_cost, quantity);


select * from order_items;

DROP TABLE IF EXISTS products_messy;
CREATE TABLE products (
  sku VARCHAR(255),
  product_name VARCHAR(255),
  category VARCHAR(255),
  is_perishable VARCHAR(255),
  shelf_life_days VARCHAR(255),
  mrp VARCHAR(255),
  unit_cost VARCHAR(255)
);
 LOAD DATA LOCAL INFILE "D:/Accio Job Data analysis/da hackathon project/New folder/products.csv" INTO TABLE products FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;

DROP TABLE IF EXISTS promo_codes_messy;
CREATE TABLE promo_codes (
  promo_code VARCHAR(255),
  discount_type VARCHAR(255),
  discount_value VARCHAR(255),
  min_order_value VARCHAR(255),
  valid_from VARCHAR(255),
  valid_to VARCHAR(255),
  applicable_stores VARCHAR(255)
);
 LOAD DATA LOCAL INFILE "D:/Accio Job Data analysis/da hackathon project/New folder/Promo_Codes.csv" INTO TABLE promo_codes FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;





