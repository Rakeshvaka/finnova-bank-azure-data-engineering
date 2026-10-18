# Interview Walkthrough — FinNova Bank

## 60–90 second summary
“I built a hands-on banking data engineering portfolio solution using Azure Data Factory, ADLS Gen2, Azure Databricks, PySpark, Delta Lake, and SQL. It follows Bronze/Silver/Gold. ADF uses a metadata control table to ingest relational sources incrementally with watermarks. Raw records land in Bronze; Databricks standardizes and validates Silver Delta tables; Gold tables provide customer, account, and transaction analytics. I designed batch audit, idempotent retries, reconciliation, and controlled backfill to reduce skipped records and duplicates. Security and operations include managed identity, Key Vault references, monitoring, and alerting.”

Use this as a practice script. Clearly distinguish simulated learning work from employer production experience.

## Common follow-ups
**Why metadata-driven ingestion?** A reusable pipeline can process many configured tables; adding sources often requires metadata rather than duplicated pipeline logic.

**When update a watermark?** After the write and validation steps succeed. Failed or partially validated batches must not advance it.

**How prevent retry duplicates?** Stable batch IDs, deterministic deduplication, business keys, and idempotent writes such as Delta `MERGE`.

**What if a record arrives three days late and lookback is 30 minutes?** Use CDC/change tracking where possible, otherwise reconciliation and controlled backfill.

**Bronze has 10 million rows and Silver has 8 million.** Confirm same batch/window; inspect filters, deduplication, joins, casts, quarantine records, and Spark logs. Reconcile business keys, fix the root cause, rerun Silver if Bronze is complete, then validate again.

**How protect secrets?** Use managed identity and Key Vault references; never commit secrets to notebooks, JSON exports, logs, or Git.
