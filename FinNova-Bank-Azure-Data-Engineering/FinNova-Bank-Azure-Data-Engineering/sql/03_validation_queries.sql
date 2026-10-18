DECLARE @lo DATETIME2(7)='2026-01-01T00:00:00';
DECLARE @hi DATETIME2(7)='2026-02-01T00:00:00';
-- Source count for a bounded extraction window
SELECT COUNT_BIG(*) AS source_rows FROM dbo.Customer
WHERE modified_date > @lo AND modified_date <= @hi;
-- Duplicate keys
SELECT customer_id, COUNT_BIG(*) AS n FROM dbo.Customer GROUP BY customer_id HAVING COUNT_BIG(*)>1;
-- Null/blank emails
SELECT customer_id,email FROM dbo.Customer WHERE email IS NULL OR LTRIM(RTRIM(email))='';
-- Invalid balances
SELECT account_id,balance FROM dbo.Account WHERE balance<0;
-- Orphan accounts
SELECT a.account_id,a.customer_id FROM dbo.Account a
WHERE NOT EXISTS (SELECT 1 FROM dbo.Customer c WHERE c.customer_id=a.customer_id);
-- Latest row per customer
WITH x AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY modified_date DESC) rn FROM dbo.Customer)
SELECT * FROM x WHERE rn=1;
