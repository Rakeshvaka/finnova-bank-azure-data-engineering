# FinNova Bank — Day 1 to Day 16 Roadmap

| Day | Focus | Validation |
|---|---|---|
| 1 | Azure foundation and metadata-driven ingestion | Control table, ADF Lookup/ForEach/Copy, Bronze output |
| 2 | Bronze-to-Silver transformation | Type casting, cleanup, deduplication, data quality |
| 3 | Gold layer and reconciliation | Aggregates and layer-to-layer counts |
| 4 | Incremental Gold maintenance | Merge/recompute strategy and totals |
| 5 | Parent orchestration | Dependencies, parameters, success/failure paths |
| 6 | Event Hubs streaming extension | Event ingestion and checkpointing concepts |
| 7 | Failure handling | Retry policy, batch audit, idempotent reruns |
| 8 | Secrets and identity | Managed Identity, Key Vault, least privilege |
| 9 | Late-arriving data and recovery | Overlap windows, backfill, reconciliation |
| 10 | Dynamic full/incremental loads | Metadata-driven branching |
| 11 | Delta history and performance | Merge behavior, partitioning, file sizing |
| 12 | SCD Type 2 | Expire old version and insert current version |
| 13 | Git and CI/CD | Source control, parameters, deployment checks |
| 14 | Monitoring | ADF diagnostics, Log Analytics, KQL alerts |
| 15 | Security, performance, cost | RBAC/ACL review, scaling and cleanup |
| 16 | Production incident/SLA recovery | Controlled replay, reconciliation, closure notes |

## Completion checklist
- [ ] Watermark advances only after success.
- [ ] Retries do not create duplicate current-state rows.
- [ ] Nulls, duplicates, invalid rows, and orphan rows are measured.
- [ ] Source-to-target reconciliation is repeatable.
- [ ] Alerts identify pipeline, activity, run ID, and error.
- [ ] Configuration is environment-parameterized.
