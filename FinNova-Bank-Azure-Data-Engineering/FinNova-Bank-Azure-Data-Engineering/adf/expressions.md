# ADF Expressions

Iterate active config rows:
```text
@activity('Lookup_Ingestion_Config').output.value
```

Current config row:
```text
@item().source_schema
@item().source_table
@item().target_container
@item().target_folder
@item().watermark_column
@item().last_watermark
```

Illustrative dynamic query construction:
```text
@concat('SELECT * FROM ', item().source_schema, '.', item().source_table)
```
This example intentionally omits the watermark predicate. Validate/whitelist metadata before using it in SQL. Prefer parameterized stored procedures. Capture a fixed upper bound and query `(lower_watermark, upper_watermark]`; commit only after success.
