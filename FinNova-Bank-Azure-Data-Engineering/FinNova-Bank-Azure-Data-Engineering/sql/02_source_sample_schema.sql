/* Synthetic source schema for local practice only. */
IF OBJECT_ID('dbo.Customer','U') IS NULL
 CREATE TABLE dbo.Customer (
 customer_id INT PRIMARY KEY, first_name VARCHAR(100), last_name VARCHAR(100),
 email VARCHAR(255), modified_date DATETIME2(7) NOT NULL);
GO
IF OBJECT_ID('dbo.Account','U') IS NULL
 CREATE TABLE dbo.Account (
 account_id INT PRIMARY KEY, customer_id INT NOT NULL, account_type VARCHAR(30) NOT NULL,
 balance DECIMAL(18,2) NOT NULL, modified_date DATETIME2(7) NOT NULL);
GO
IF OBJECT_ID('dbo.Transaction','U') IS NULL
 CREATE TABLE dbo.[Transaction] (
 transaction_id BIGINT PRIMARY KEY, account_id INT NOT NULL, transaction_date DATETIME2(7) NOT NULL,
 amount DECIMAL(18,2) NOT NULL, transaction_type VARCHAR(30) NOT NULL, modified_date DATETIME2(7) NOT NULL);
GO
IF NOT EXISTS (SELECT 1 FROM dbo.Customer WHERE customer_id=1011)
 INSERT dbo.Customer VALUES
 (1011,'Asha','Rao','asha.example@example.com','2026-01-01T09:00:00'),
 (1013,'Vikram','Shah','vikram.example@example.com','2026-01-02T10:00:00'),
 (1014,'Neha','Iyer','neha.example@example.com','2026-01-03T11:00:00');
GO
