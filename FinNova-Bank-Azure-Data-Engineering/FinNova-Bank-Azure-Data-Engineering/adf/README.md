# ADF Template Notes

The JSON is an illustrative design template, not a complete direct-import export. Create linked services, datasets, integration runtime references, parameters, and credentials in your own factory.

Suggested flow: Lookup active config rows → ForEach → Copy to Bronze → capture upper watermark → validate completion → update batch audit → commit watermark only after success. Failure path records failure and does not advance watermark.

Use stable batch IDs, fixed upper bounds, safe metadata validation, and idempotent writes. Do not interpolate arbitrary untrusted metadata into source SQL.
