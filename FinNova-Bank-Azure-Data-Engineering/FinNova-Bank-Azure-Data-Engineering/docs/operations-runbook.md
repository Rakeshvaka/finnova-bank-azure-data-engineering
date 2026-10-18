# Operations Runbook

## Pipeline succeeded, but records are missing
1. Confirm source table, batch ID, and extraction window.
2. Compare counts at Source, Bronze, Silver, and Gold for the same window.
3. Inspect ADF Monitor: rows read/written, source query, warnings, duration.
4. Check committed watermark and batch upper bound.
5. If Bronze is complete but Silver is short, inspect filters, deduplication keys, joins, casts, and quarantined rows.
6. Fix the root cause and rerun only the affected layer if upstream data is complete.
7. Reconcile counts and business keys after recovery.

## Watermark update failed after Bronze succeeded
Check the batch audit. Do not blindly start a new logical batch or advance the watermark. Reuse the batch ID or safely replay the same interval, confirm idempotency, and retry the watermark commit only after success criteria pass.

## Retry created duplicates
Compare duplicate keys and batch IDs. Confirm grain and deterministic ordering. Deduplicate the affected range, use Delta `MERGE` keyed by business key, validate uniqueness and totals, then make the stage idempotent before automatic retries.

## Record arrives three days late, beyond a 30-minute lookback
The overlap misses it. Use CDC/change tracking where possible, or periodic reconciliation/backfill. Reprocess idempotently and verify business keys. Do not move the watermark backward without a controlled recovery plan.

## ADF 403 / permission failure
Identify runtime identity and target operation. Verify RBAC scope, ADLS Gen2 ACLs on every required path, and firewall/private endpoint rules. Grant least privilege and retest using the same identity.

## Slow Copy Activity
Compare rows/bytes, source query duration, sink throughput, and Integration Runtime utilization. Inspect indexes and predicate selectivity. Tune parallelism only after confirming source/sink capacity; record before/after runtime and counts.

## Incident closure
Record incident time, pipeline and batch IDs, impact, root cause, recovery, reconciled counts, and prevention actions.
