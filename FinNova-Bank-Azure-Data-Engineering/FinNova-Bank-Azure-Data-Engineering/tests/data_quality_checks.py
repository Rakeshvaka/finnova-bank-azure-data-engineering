# PySpark data-quality assertions.
from pyspark.sql import functions as F

def assert_no_nulls(df, columns):
    failures = {c: df.filter(F.col(c).isNull()).count() for c in columns}
    failures = {k:v for k,v in failures.items() if v}
    if failures:
        raise AssertionError(f"Null check failed: {failures}")

def assert_unique_key(df, key_columns):
    duplicates = df.groupBy(*key_columns).count().filter(F.col("count") > 1)
    sample = duplicates.limit(10).collect()
    if sample:
        raise AssertionError(f"Duplicate key check failed for {key_columns}: {sample}")

def assert_no_orphans(child_df, parent_df, child_key, parent_key):
    orphans = child_df.join(parent_df.select(F.col(parent_key).alias("_parent_key")),
      F.col(child_key)==F.col("_parent_key"), "left_anti")
    sample = orphans.select(child_key).limit(10).collect()
    if sample:
        raise AssertionError(f"Orphan check failed for {child_key}: {sample}")
