# SCD Type 2 pattern. Validate rerun semantics in a disposable workspace first.
from delta.tables import DeltaTable
from pyspark.sql import functions as F
storage_account = "<storage-account>"
target_path = f"abfss://gold@{storage_account}.dfs.core.windows.net/dim_customer/"
source = (df_customer_changes.select("customer_id","first_name","last_name","email","modified_date")
 .withColumn("effective_from",F.col("modified_date").cast("timestamp"))
 .withColumn("effective_to",F.lit(None).cast("timestamp"))
 .withColumn("is_current",F.lit(True)))
if not DeltaTable.isDeltaTable(spark,target_path):
 source.write.format("delta").mode("overwrite").save(target_path)
else:
 target = DeltaTable.forPath(spark,target_path)
 changed = """t.is_current=true AND (
 NOT (t.first_name <=> s.first_name) OR
 NOT (t.last_name <=> s.last_name) OR
 NOT (t.email <=> s.email))"""
 (target.alias("t").merge(source.alias("s"),"t.customer_id=s.customer_id")
  .whenMatchedUpdate(condition=changed,set={"effective_to":"s.effective_from","is_current":"false"}).execute())
 current = spark.read.format("delta").load(target_path).filter("is_current=true")
 inserts = source.alias("s").join(current.select("customer_id").alias("t"),
  F.col("s.customer_id")==F.col("t.customer_id"),"left_anti")
 if inserts.limit(1).count():
  inserts.write.format("delta").mode("append").save(target_path)
current_dim = spark.read.format("delta").load(target_path).filter("is_current=true")
if current_dim.groupBy("customer_id").count().filter("count>1").limit(1).count():
 raise ValueError("SCD2 validation failed: multiple current rows per customer")
