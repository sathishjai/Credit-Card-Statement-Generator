-- Create DB and tables
CREATE DATABASE IF NOT EXISTS cimb_db;
USE cimb_db;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    address TEXT,
    card_number VARCHAR(16),
    account_number VARCHAR(20),
    credit_limit DECIMAL(10,2),
    available_credit DECIMAL(10,2)
);

-- Statements table
CREATE TABLE IF NOT EXISTS statements (
    statement_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    statement_date DATE,
    period_start DATE,
    period_end DATE,
    outstanding_balance DECIMAL(10,2),
    minimum_due DECIMAL(10,2),
    due_date DATE,
    reward_points INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    statement_id INT,
    txn_date DATE,
    description VARCHAR(255),
    amount DECIMAL(10,2),
    txn_type ENUM('Payment', 'Purchase', 'Interest', 'Fee', 'Cash Advance'),
    FOREIGN KEY (statement_id) REFERENCES statements(statement_id)
);

-- Sample data
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('John Smith', '123 Sample Street\nKuala Lumpur, 50450\nMalaysia', '1234567812345678', '1234567890', 30000.00, 24562.35);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(1, '2025-04-10', '2025-03-11', '2025-04-10', 5437.65, 271.88, '2025-05-01', 12450);

-- Generate 20 transactions
INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(1, '2025-03-11', 'Opening Balance', 4837.21, 'Purchase'),
(1, '2025-03-12', 'Payment Received', -1500.00, 'Payment'),
(1, '2025-03-13', 'Grocery Purchase', 125.40, 'Purchase'),
(1, '2025-03-14', 'Online Shopping', 258.99, 'Purchase'),
(1, '2025-03-15', 'Restaurant', 134.20, 'Purchase'),
(1, '2025-03-16', 'Interest Charge', 44.00, 'Interest'),
(1, '2025-03-17', 'Pharmacy', 88.00, 'Purchase'),
(1, '2025-03-18', 'Movie Tickets', 36.00, 'Purchase'),
(1, '2025-03-19', 'Coffee Shop', 21.50, 'Purchase'),
(1, '2025-03-20', 'App Store', 15.99, 'Purchase'),
(1, '2025-03-21', 'E-wallet Top-up', 200.00, 'Purchase'),
(1, '2025-03-22', 'Gym Membership', 299.00, 'Purchase'),
(1, '2025-03-23', 'Bookstore', 65.00, 'Purchase'),
(1, '2025-03-24', 'Ride Sharing', 42.80, 'Purchase'),
(1, '2025-03-25', 'Clothing Store', 430.00, 'Purchase'),
(1, '2025-03-26', 'Fuel Station', 110.00, 'Purchase'),
(1, '2025-03-27', 'Electricity Bill', 240.00, 'Purchase'),
(1, '2025-03-28', 'Water Bill', 70.00, 'Purchase'),
(1, '2025-03-29', 'Internet Bill', 100.00, 'Purchase'),
(1, '2025-03-30', 'Mobile Bill', 100.00, 'Purchase');




-- Customer 2
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Alice Tan', '456 Jalan Bunga Raya\nPenang, 10450\nMalaysia', '4321432143214321', '2345678901', 25000.00, 19876.10);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(2, '2025-04-10', '2025-03-11', '2025-04-10', 5123.90, 256.20, '2025-05-01', 11200);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(2, '2025-03-11', 'Opening Balance', 4523.50, 'Purchase'),
(2, '2025-03-12', 'Payment Received', -1000.00, 'Payment'),
(2, '2025-03-13', 'Supermarket', 140.00, 'Purchase'),
(2, '2025-03-14', 'Clothing Store', 220.50, 'Purchase'),
(2, '2025-03-15', 'Streaming Service', 30.00, 'Purchase'),
(2, '2025-03-16', 'Interest Charge', 40.00, 'Interest'),
(2, '2025-03-17', 'Electronics', 300.00, 'Purchase'),
(2, '2025-03-18', 'Ride Sharing', 35.00, 'Purchase'),
(2, '2025-03-19', 'Bookstore', 58.90, 'Purchase'),
(2, '2025-03-20', 'Petrol Station', 100.00, 'Purchase'),
(2, '2025-03-21', 'Phone Bill', 95.00, 'Purchase'),
(2, '2025-03-22', 'Internet Bill', 85.00, 'Purchase'),
(2, '2025-03-23', 'Cafe', 20.00, 'Purchase'),
(2, '2025-03-24', 'Mobile Accessories', 45.50, 'Purchase'),
(2, '2025-03-25', 'Travel Booking', 600.00, 'Purchase'),
(2, '2025-03-26', 'Hotel Stay', 750.00, 'Purchase'),
(2, '2025-03-27', 'Restaurant', 130.00, 'Purchase'),
(2, '2025-03-28', 'E-wallet Top-up', 150.00, 'Purchase'),
(2, '2025-03-29', 'Pharmacy', 90.00, 'Purchase'),
(2, '2025-03-30', 'Utilities', 100.00, 'Purchase');

-- Customer 3
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Michael Lee', '789 Taman Damai\nJohor Bahru, 80000\nMalaysia', '5678567856785678', '3456789012', 40000.00, 36250.75);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(3, '2025-04-10', '2025-03-11', '2025-04-10', 3750.25, 187.52, '2025-05-01', 9300);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(3, '2025-03-11', 'Opening Balance', 3000.00, 'Purchase'),
(3, '2025-03-12', 'Payment Received', -500.00, 'Payment'),
(3, '2025-03-13', 'Gadget Store', 800.00, 'Purchase'),
(3, '2025-03-14', 'Convenience Store', 50.00, 'Purchase'),
(3, '2025-03-15', 'Gas Station', 120.00, 'Purchase'),
(3, '2025-03-16', 'Interest Charge', 30.00, 'Interest'),
(3, '2025-03-17', 'Restaurant', 200.00, 'Purchase'),
(3, '2025-03-18', 'Taxi Ride', 35.00, 'Purchase'),
(3, '2025-03-19', 'App Purchase', 12.99, 'Purchase'),
(3, '2025-03-20', 'Laundry Service', 25.00, 'Purchase'),
(3, '2025-03-21', 'Groceries', 150.00, 'Purchase'),
(3, '2025-03-22', 'Hardware Store', 98.00, 'Purchase'),
(3, '2025-03-23', 'Water Bill', 70.00, 'Purchase'),
(3, '2025-03-24', 'Electricity Bill', 250.00, 'Purchase'),
(3, '2025-03-25', 'Mobile Bill', 100.00, 'Purchase'),
(3, '2025-03-26', 'Travel Insurance', 180.00, 'Purchase'),
(3, '2025-03-27', 'Spa', 90.00, 'Purchase'),
(3, '2025-03-28', 'Online Shopping', 500.00, 'Purchase'),
(3, '2025-03-29', 'Gift Shop', 80.00, 'Purchase'),
(3, '2025-03-30', 'Charity Donation', 50.00, 'Purchase');

-- Customer 4
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Nur Aisyah', '11 Lorong Kenanga\nKota Kinabalu, 88300\nMalaysia', '9876987698769876', '4567890123', 20000.00, 14500.40);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(4, '2025-04-10', '2025-03-11', '2025-04-10', 5499.60, 274.98, '2025-05-01', 7800);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(4, '2025-03-11', 'Opening Balance', 4000.00, 'Purchase'),
(4, '2025-03-12', 'Payment Received', -500.00, 'Payment'),
(4, '2025-03-13', 'Groceries', 150.00, 'Purchase'),
(4, '2025-03-14', 'Fashion Store', 200.00, 'Purchase'),
(4, '2025-03-15', 'Pharmacy', 80.00, 'Purchase'),
(4, '2025-03-16', 'Interest Charge', 45.00, 'Interest'),
(4, '2025-03-17', 'Bookstore', 60.00, 'Purchase'),
(4, '2025-03-18', 'Taxi', 25.00, 'Purchase'),
(4, '2025-03-19', 'Restaurant', 180.00, 'Purchase'),
(4, '2025-03-20', 'Online Streaming', 25.00, 'Purchase'),
(4, '2025-03-21', 'Hair Salon', 110.00, 'Purchase'),
(4, '2025-03-22', 'Fuel', 90.00, 'Purchase'),
(4, '2025-03-23', 'Mobile Accessories', 55.00, 'Purchase'),
(4, '2025-03-24', 'Water Bill', 65.00, 'Purchase'),
(4, '2025-03-25', 'Electricity Bill', 230.00, 'Purchase'),
(4, '2025-03-26', 'Internet Bill', 95.00, 'Purchase'),
(4, '2025-03-27', 'Charity', 50.00, 'Purchase'),
(4, '2025-03-28', 'Pet Care', 75.00, 'Purchase'),
(4, '2025-03-29', 'E-wallet Top-up', 250.00, 'Purchase'),
(4, '2025-03-30', 'Travel Booking', 900.60, 'Purchase');

-- Customer 5
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Amirul Hakim', '5 Jalan Tun Razak\nMelaka, 75450\nMalaysia', '8765432187654321', '5678901234', 35000.00, 27000.00);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(5, '2025-04-10', '2025-03-11', '2025-04-10', 8000.00, 400.00, '2025-05-01', 10200);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(5, '2025-03-11', 'Opening Balance', 7000.00, 'Purchase'),
(5, '2025-03-12', 'Payment Received', -2000.00, 'Payment'),
(5, '2025-03-13', 'Electronics', 1000.00, 'Purchase'),
(5, '2025-03-14', 'Furniture', 1500.00, 'Purchase'),
(5, '2025-03-15', 'Petrol Station', 100.00, 'Purchase'),
(5, '2025-03-16', 'Interest Charge', 50.00, 'Interest'),
(5, '2025-03-17', 'Cinema', 45.00, 'Purchase'),
(5, '2025-03-18', 'Streaming Service', 30.00, 'Purchase'),
(5, '2025-03-19', 'Groceries', 180.00, 'Purchase'),
(5, '2025-03-20', 'Flight Ticket', 900.00, 'Purchase'),
(5, '2025-03-21', 'Clothing', 400.00, 'Purchase'),
(5, '2025-03-22', 'Mobile Bill', 100.00, 'Purchase'),
(5, '2025-03-23', 'Restaurant', 250.00, 'Purchase'),
(5, '2025-03-24', 'Hotel Booking', 1200.00, 'Purchase'),
(5, '2025-03-25', 'Water Bill', 75.00, 'Purchase'),
(5, '2025-03-26', 'Electricity Bill', 180.00, 'Purchase'),
(5, '2025-03-27', 'Pharmacy', 90.00, 'Purchase'),
(5, '2025-03-28', 'Taxi Ride', 35.00, 'Purchase'),
(5, '2025-03-29', 'E-wallet Top-up', 300.00, 'Purchase'),
(5, '2025-03-30', 'Gym Membership', 120.00, 'Purchase');



-- Customer 6
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Farah Zainal', '88 Jalan Merdeka\nShah Alam, 40000\nMalaysia', '1234432112344321', '6789012345', 30000.00, 22500.50);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(6, '2025-04-10', '2025-03-11', '2025-04-10', 7499.50, 375.00, '2025-05-01', 11500);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(6, '2025-03-11', 'Opening Balance', 6000.00, 'Purchase'),
(6, '2025-03-12', 'Payment Received', -1000.00, 'Payment'),
(6, '2025-03-13', 'Grocery Store', 220.00, 'Purchase'),
(6, '2025-03-14', 'Fashion Store', 330.00, 'Purchase'),
(6, '2025-03-15', 'Pharmacy', 90.00, 'Purchase'),
(6, '2025-03-16', 'Interest Charge', 55.00, 'Interest'),
(6, '2025-03-17', 'Restaurant', 200.00, 'Purchase'),
(6, '2025-03-18', 'Movie Night', 45.00, 'Purchase'),
(6, '2025-03-19', 'Fuel Station', 110.00, 'Purchase'),
(6, '2025-03-20', 'Online Shopping', 175.00, 'Purchase'),
(6, '2025-03-21', 'Phone Bill', 95.00, 'Purchase'),
(6, '2025-03-22', 'Internet Bill', 80.00, 'Purchase'),
(6, '2025-03-23', 'Water Bill', 70.00, 'Purchase'),
(6, '2025-03-24', 'Electricity Bill', 150.00, 'Purchase'),
(6, '2025-03-25', 'E-wallet Top-up', 300.00, 'Purchase'),
(6, '2025-03-26', 'Hotel Booking', 1000.00, 'Purchase'),
(6, '2025-03-27', 'Air Ticket', 600.00, 'Purchase'),
(6, '2025-03-28', 'Bookstore', 85.00, 'Purchase'),
(6, '2025-03-29', 'Hair Salon', 120.00, 'Purchase'),
(6, '2025-03-30', 'Spa Treatment', 164.50, 'Purchase');

-- Customer 7
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Daniel Wong', '42 Jalan Kasturi\nIpoh, 31400\nMalaysia', '4444333344443333', '7890123456', 25000.00, 16200.80);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(7, '2025-04-10', '2025-03-11', '2025-04-10', 8799.20, 439.95, '2025-05-01', 13560);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(7, '2025-03-11', 'Opening Balance', 7000.00, 'Purchase'),
(7, '2025-03-12', 'Payment Received', -1200.00, 'Payment'),
(7, '2025-03-13', 'Supermarket', 150.00, 'Purchase'),
(7, '2025-03-14', 'Mobile Top-up', 50.00, 'Purchase'),
(7, '2025-03-15', 'Streaming Service', 30.00, 'Purchase'),
(7, '2025-03-16', 'Interest Charge', 45.00, 'Interest'),
(7, '2025-03-17', 'Flight Ticket', 800.00, 'Purchase'),
(7, '2025-03-18', 'Taxi Ride', 25.00, 'Purchase'),
(7, '2025-03-19', 'Electronics', 950.00, 'Purchase'),
(7, '2025-03-20', 'Pet Shop', 85.00, 'Purchase'),
(7, '2025-03-21', 'Bookstore', 60.00, 'Purchase'),
(7, '2025-03-22', 'Gym Membership', 240.00, 'Purchase'),
(7, '2025-03-23', 'Online Subscription', 40.00, 'Purchase'),
(7, '2025-03-24', 'Furniture Store', 900.00, 'Purchase'),
(7, '2025-03-25', 'Haircut', 70.00, 'Purchase'),
(7, '2025-03-26', 'Clothing Store', 350.00, 'Purchase'),
(7, '2025-03-27', 'Internet Bill', 85.00, 'Purchase'),
(7, '2025-03-28', 'Water Bill', 60.00, 'Purchase'),
(7, '2025-03-29', 'Electricity Bill', 240.00, 'Purchase'),
(7, '2025-03-30', 'Gift Shop', 80.20, 'Purchase');

-- Customer 8
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Siti Nabila', '20 Jalan Cempaka\nSeremban, 70200\nMalaysia', '5678123456781234', '8901234567', 18000.00, 10950.00);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(8, '2025-04-10', '2025-03-11', '2025-04-10', 7050.00, 352.50, '2025-05-01', 9100);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(8, '2025-03-11', 'Opening Balance', 6000.00, 'Purchase'),
(8, '2025-03-12', 'Payment Received', -1000.00, 'Payment'),
(8, '2025-03-13', 'Shopping Mall', 500.00, 'Purchase'),
(8, '2025-03-14', 'Café', 55.00, 'Purchase'),
(8, '2025-03-15', 'Restaurant', 140.00, 'Purchase'),
(8, '2025-03-16', 'Interest Charge', 35.00, 'Interest'),
(8, '2025-03-17', 'Petrol Station', 90.00, 'Purchase'),
(8, '2025-03-18', 'Online Shopping', 420.00, 'Purchase'),
(8, '2025-03-19', 'Electricity Bill', 180.00, 'Purchase'),
(8, '2025-03-20', 'Internet Bill', 70.00, 'Purchase'),
(8, '2025-03-21', 'Water Bill', 65.00, 'Purchase'),
(8, '2025-03-22', 'Groceries', 250.00, 'Purchase'),
(8, '2025-03-23', 'Streaming Service', 25.00, 'Purchase'),
(8, '2025-03-24', 'Fashion Store', 300.00, 'Purchase'),
(8, '2025-03-25', 'Phone Bill', 95.00, 'Purchase'),
(8, '2025-03-26', 'Pharmacy', 75.00, 'Purchase'),
(8, '2025-03-27', 'Movie Night', 40.00, 'Purchase'),
(8, '2025-03-28', 'Hotel Booking', 650.00, 'Purchase'),
(8, '2025-03-29', 'Flight Booking', 900.00, 'Purchase'),
(8, '2025-03-30', 'Souvenir Shop', 95.00, 'Purchase');

-- Customer 9
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Arun Kumar', '31 Jalan Perlis\nAlor Setar, 05000\nMalaysia', '8765876587658765', '9012345678', 22000.00, 14900.75);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(9, '2025-04-10', '2025-03-11', '2025-04-10', 7100.25, 355.00, '2025-05-01', 10400);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(9, '2025-03-11', 'Opening Balance', 6200.00, 'Purchase'),
(9, '2025-03-12', 'Payment Received', -800.00, 'Payment'),
(9, '2025-03-13', 'Restaurant', 120.00, 'Purchase'),
(9, '2025-03-14', 'Mobile Bill', 90.00, 'Purchase'),
(9, '2025-03-15', 'Streaming', 35.00, 'Purchase'),
(9, '2025-03-16', 'Interest Charge', 55.00, 'Interest'),
(9, '2025-03-17', 'Clothing Store', 400.00, 'Purchase'),
(9, '2025-03-18', 'Supermarket', 160.00, 'Purchase'),
(9, '2025-03-19', 'Fuel', 100.00, 'Purchase'),
(9, '2025-03-20', 'Taxi Ride', 25.00, 'Purchase'),
(9, '2025-03-21', 'Air Ticket', 800.00, 'Purchase'),
(9, '2025-03-22', 'Furniture', 900.00, 'Purchase'),
(9, '2025-03-23', 'Water Bill', 70.00, 'Purchase'),
(9, '2025-03-24', 'Electricity Bill', 190.00, 'Purchase'),
(9, '2025-03-25', 'Internet', 85.00, 'Purchase'),
(9, '2025-03-26', 'Cafe', 45.00, 'Purchase'),
(9, '2025-03-27', 'E-wallet Top-up', 250.00, 'Purchase'),
(9, '2025-03-28', 'Hotel Stay', 700.00, 'Purchase'),
(9, '2025-03-29', 'Gift Shop', 100.00, 'Purchase'),
(9, '2025-03-30', 'Pharmacy', 70.25, 'Purchase');

-- Customer 10
INSERT INTO customers (name, address, card_number, account_number, credit_limit, available_credit)
VALUES
('Tan Mei Ling', '19 Jalan Mahsuri\nKuantan, 25200\nMalaysia', '3333222233332222', '0123456789', 26000.00, 19125.60);

INSERT INTO statements (customer_id, statement_date, period_start, period_end, outstanding_balance, minimum_due, due_date, reward_points)
VALUES
(10, '2025-04-10', '2025-03-11', '2025-04-10', 6874.40, 343.70, '2025-05-01', 9870);

INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type) VALUES
(10, '2025-03-11', 'Opening Balance', 5800.00, 'Purchase'),
(10, '2025-03-12', 'Payment Received', -1000.00, 'Payment'),
(10, '2025-03-13', 'Supermarket', 130.00, 'Purchase'),
(10, '2025-03-14', 'Hair Salon', 95.00, 'Purchase'),
(10, '2025-03-15', 'Petrol Station', 110.00, 'Purchase'),
(10, '2025-03-16', 'Interest Charge', 45.00, 'Interest'),
(10, '2025-03-17', 'Streaming Subscription', 25.00, 'Purchase'),
(10, '2025-03-18', 'Online Shopping', 400.00, 'Purchase'),
(10, '2025-03-19', 'Groceries', 180.00, 'Purchase'),
(10, '2025-03-20', 'Taxi Ride', 35.00, 'Purchase'),
(10, '2025-03-21', 'Furniture Store', 850.00, 'Purchase'),
(10, '2025-03-22', 'Bookstore', 70.00, 'Purchase'),
(10, '2025-03-23', 'Hotel Booking', 950.00, 'Purchase'),
(10, '2025-03-24', 'Water Bill', 65.00, 'Purchase'),
(10, '2025-03-25', 'Electricity Bill', 170.00, 'Purchase'),
(10, '2025-03-26', 'Internet Bill', 85.00, 'Purchase'),
(10, '2025-03-27', 'Mobile Top-up', 50.00, 'Purchase'),
(10, '2025-03-28', 'Restaurant', 240.00, 'Purchase'),
(10, '2025-03-29', 'E-wallet Top-up', 300.00, 'Purchase'),
(10, '2025-03-30', 'Gym Membership', 139.40, 'Purchase');


