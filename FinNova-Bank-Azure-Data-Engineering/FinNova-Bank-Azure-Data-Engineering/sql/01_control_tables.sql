/* SQL Server/Azure SQL example. Run in a development database. */
IF OBJECT_ID('dbo.ingestion_config','U') IS NULL
BEGIN
 CREATE TABLE dbo.ingestion_config (
  config_id INT IDENTITY(1,1) PRIMARY KEY,
  source_system VARCHAR(100) NOT NULL,
  source_schema SYSNAME NOT NULL,
  source_table SYSNAME NOT NULL,
  watermark_column SYSNAME NULL,
  last_watermark DATETIME2(7) NULL,
  target_container VARCHAR(100) NOT NULL,
  target_folder VARCHAR(500) NOT NULL,
  load_type VARCHAR(20) NOT NULL CHECK (load_type IN ('FULL','INCREMENTAL')),
  is_active BIT NOT NULL DEFAULT (1),
  created_date DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
  modified_date DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME()
 );
END;
GO
IF OBJECT_ID('dbo.ingestion_batch_audit','U') IS NULL
BEGIN
 CREATE TABLE dbo.ingestion_batch_audit (
  batch_id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
  pipeline_name VARCHAR(200) NOT NULL,
  source_system VARCHAR(100) NOT NULL,
  source_schema SYSNAME NOT NULL,
  source_table SYSNAME NOT NULL,
  lower_watermark DATETIME2(7) NULL,
  upper_watermark DATETIME2(7) NULL,
  status VARCHAR(20) NOT NULL CHECK (status IN ('STARTED','SUCCEEDED','FAILED','RECOVERING')),
  rows_read BIGINT NULL, rows_written BIGINT NULL,
  error_message NVARCHAR(4000) NULL,
  started_utc DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME(),
  completed_utc DATETIME2(7) NULL
 );
END;
GO
IF NOT EXISTS (SELECT 1 FROM dbo.ingestion_config WHERE source_system='BankingDB' AND source_schema='dbo' AND source_table='Customer')
BEGIN
 INSERT dbo.ingestion_config
 (source_system,source_schema,source_table,watermark_column,last_watermark,target_container,target_folder,load_type)
 VALUES
 ('BankingDB','dbo','Customer','modified_date','1900-01-01','bronze','banking/customer','INCREMENTAL'),
 ('BankingDB','dbo','Account','modified_date','1900-01-01','bronze','banking/account','INCREMENTAL'),
 ('BankingDB','dbo','Transaction','modified_date','1900-01-01','bronze','banking/transaction','INCREMENTAL');
END;
GO
