DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS pay CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS process CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS workplace CASCADE;
DROP TABLE IF EXISTS works CASCADE;
DROP TABLE IF EXISTS office CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS contains CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS delivery CASCADE;

CREATE TABLE customer(
cust_no INTEGER PRIMARY KEY,
name VARCHAR(80) NOT NULL,
email VARCHAR(254) UNIQUE NOT NULL,
phone VARCHAR(15),
address VARCHAR(255)
);

CREATE TABLE orders(
order_no INTEGER PRIMARY KEY,
cust_no INTEGER NOT NULL REFERENCES customer,
date DATE NOT NULL
--order_no must exist in contains
);

CREATE TABLE pay(
order_no INTEGER PRIMARY KEY REFERENCES orders,
cust_no INTEGER NOT NULL REFERENCES customer
);

CREATE TABLE employee(
ssn VARCHAR(20) PRIMARY KEY,
TIN VARCHAR(20) UNIQUE NOT NULL,
bdate DATE,
name VARCHAR NOT NULL
--age must be >=18
);

CREATE TABLE process(
ssn VARCHAR(20) REFERENCES employee,
order_no INTEGER REFERENCES orders,
PRIMARY KEY (ssn, order_no)
);

CREATE TABLE department(
name VARCHAR PRIMARY KEY
);

CREATE TABLE workplace(
address VARCHAR PRIMARY KEY,
lat NUMERIC(8, 6) NOT NULL,
long NUMERIC(9, 6) NOT NULL,
UNIQUE(lat, long)
--address must be in warehouse or office but not both
);

CREATE TABLE office(
address VARCHAR(255) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE warehouse(
address VARCHAR(255) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE works(
ssn VARCHAR(20) REFERENCES employee,
name VARCHAR(200) REFERENCES department,
address VARCHAR(255) REFERENCES workplace,
PRIMARY KEY (ssn, name, address)
);

CREATE TABLE product(
SKU VARCHAR(25) PRIMARY KEY,
name VARCHAR(200) NOT NULL,
description VARCHAR,
price NUMERIC(10, 2) NOT NULL,
ean NUMERIC(13) UNIQUE
);

CREATE TABLE contains(
order_no INTEGER REFERENCES orders,
SKU VARCHAR(25) REFERENCES product,
qty INTEGER,
PRIMARY KEY (order_no, SKU)
);

CREATE TABLE supplier(
TIN VARCHAR(20) PRIMARY KEY,
name VARCHAR(200),
address VARCHAR(255),
SKU VARCHAR(25) REFERENCES product,
date DATE
);

CREATE TABLE delivery(
address VARCHAR(255) REFERENCES warehouse,
TIN VARCHAR(20) REFERENCES supplier,
PRIMARY KEY (address, TIN)
);



INSERT INTO customer (cust_no, name, email, phone, address)
VALUES (1, 'Cliente A', 'clienteA@example.com', '123456789', '1000-008 Lisboa'),
       (2, 'Cliente B', 'clienteB@example.com', '987654321', '4000-053 Porto'),
       (3, 'Cliente C', 'clienteC@example.com', '456789123', '3000-030 Coimbra'),
       (4, 'Cliente D', 'clienteD@example.com', '987654321', '8000-073 Faro'),
       (5, 'Cliente E', 'clienteE@example.com', '123456789', '4700-024 Braga');
       
INSERT INTO orders (order_no, cust_no, date)
VALUES (1, 1, '2022-01-10'),
       (2, 1, '2022-02-15'),
       (3, 2, '2022-01-05'),
       (4, 3, '2022-03-20'),
       (5, 3, '2022-04-12'),
       (6, 4, '2022-01-10'),
       (7, 4, '2022-02-15'),
       (8, 5, '2022-01-05'),
       (9, 5, '2022-03-20'),
       (10, 5, '2022-04-12');

INSERT INTO pay (order_no, cust_no)
VALUES (1, 1),
       (2, 1),
       (3, 2),
       (4, 3),
       (5, 3),
       (6, 4),
       (7, 4);

INSERT INTO employee (ssn, TIN, bdate, name)
VALUES ('SSN001', 'TIN001', '1990-05-15', 'Employee A'),
       ('SSN002', 'TIN002', '1985-08-20', 'Employee B'),
       ('SSN003', 'TIN003', '1992-02-10', 'Employee C'),
       ('SSN004', 'TIN004', '1987-07-25', 'Employee D'),
       ('SSN005', 'TIN005', '1993-12-05', 'Employee E');

INSERT INTO process (ssn, order_no)
VALUES ('SSN001', 1),
       ('SSN001', 2),
       ('SSN002', 2),
       ('SSN002', 3),
       ('SSN003', 4),
       ('SSN003', 5),
       ('SSN005', 1);
       --Problem dois employyes processarem a mesma oorder?

INSERT INTO product (SKU, name, description, price, ean)
VALUES ('SKU001', 'Produto 1', 'Descrição do Produto 1', 10.99, 1234567890123),
       ('SKU002', 'Produto 2', 'Descrição do Produto 2', 19.99, 9876543210987),
       ('SKU003', 'Produto 3', 'Descrição do Produto 3', 5.99, 5678901234567);

INSERT INTO contains (order_no, SKU, qty)
VALUES (1, 'SKU001', 2),
       (1, 'SKU002', 1),
       (2, 'SKU003', 3),
       (2, 'SKU001', 1),
       (2, 'SKU002', 2),
       (3, 'SKU001', 5),
       (3, 'SKU002', 3),
       (3, 'SKU003', 6),
       (4, 'SKU003', 4),
       (4, 'SKU001', 3),
       (4, 'SKU002', 2),
       (5, 'SKU001', 2),
       (5, 'SKU002', 1),
       (5, 'SKU003', 2),
       (6, 'SKU003', 1),
       (7, 'SKU003', 1),
       (8, 'SKU003', 1),
       (9, 'SKU003', 1),
       (10, 'SKU003', 1);
       
INSERT INTO workplace (address, lat, long)
VALUES
  ('1000-048 Lisboa', 40.123456, -74.123456),
  ('4000-033 Porto', 40.654321, -74.654321),
  ('4700-012 Braga', 40.987654, -74.987654);

-- Inserting sample data into the office table
INSERT INTO office (address)
VALUES
  ('1000-048 Lisboa');

-- Inserting sample data into the warehouse table
INSERT INTO warehouse (address)
VALUES
  ('4000-033 Porto'),
  ('4700-012 Braga');

INSERT INTO supplier (TIN, name, address, SKU, date)
VALUES
  ('S1', 'Supplier 1', '4000-033 Porto', 'SKU001', '06-01-2022'),
  ('S2', 'Supplier 2', '4000-033 Porto', 'SKU002', '08-01-2022'),
  ('S4', 'Supplier 4', '4000-033 Porto', 'SKU001', '10-02-2022');