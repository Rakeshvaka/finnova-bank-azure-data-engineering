# Architecture and Data Flow

## Sources
Relational tables such as Customer, Account, Transaction; REST APIs and files can use the same metadata pattern. Event Hubs is an optional streaming extension.

## Ingestion and control plane
ADF reads active configuration rows, iterates through sources, and copies raw data to ADLS Gen2. Track each run with a stable batch ID and audit fields for source, window, status, counts, and errors.

## Medallion layers
- **Bronze:** raw source-aligned data, batch ID, ingestion timestamp, source path.
- **Silver:** normalized types, deduplication, null/duplicate checks, referential checks, and quarantined invalid records.
- **Gold:** business datasets such as Customer 360, account balance summaries, and monthly transaction aggregates.

## Incremental contract
1. Read the committed watermark.
2. Capture a fixed upper bound for the batch where possible.
3. Extract `(lower_watermark, upper_watermark]`.
4. Write Bronze and record batch status.
5. Validate expected counts and completion status.
6. Commit the watermark only after success criteria pass.

A timestamp may not be unique; use a composite cursor such as `(modified_date, primary_key)` or CDC/change tracking where available. A lookback window cannot detect arbitrary older updates by itself.

## Retry contract
Keep each stage idempotent; reuse batch IDs; do not advance watermarks after failure; reprocess only affected layers; use Delta `MERGE` or deterministic partition replacement; reconcile counts and business keys Source → Bronze → Silver → Gold.
