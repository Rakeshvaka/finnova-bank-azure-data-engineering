# Databricks / PySpark example: Bronze -> Silver. Replace paths and source format.
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

storage_account = "<storage-account>"
bronze_path = f"abfss://bronze@{storage_account}.dfs.core.windows.net/banking/customer/"
silver_path = f"abfss://silver@{storage_account}.dfs.core.windows.net/banking/customer/"
quarantine_path = f"abfss://quarantine@{storage_account}.dfs.core.windows.net/banking/customer/"

df_bronze = spark.read.format("parquet").load(bronze_path)
required = {"customer_id", "modified_date"}
missing = required - set(df_bronze.columns)
if missing:
    raise ValueError(f"Required columns missing: {sorted(missing)}")

df = (df_bronze.withColumn("customer_id", F.col("customer_id").cast("long"))
      .withColumn("first_name", F.trim(F.col("first_name")))
      .withColumn("last_name", F.trim(F.col("last_name")))
      .withColumn("email", F.lower(F.trim(F.col("email"))))
      .withColumn("modified_date", F.to_timestamp("modified_date"))
      .withColumn("ingestion_timestamp", F.current_timestamp()))
invalid = F.col("customer_id").isNull() | F.col("modified_date").isNull()
bad = df.filter(invalid).withColumn("dq_reason", F.lit("Missing customer_id or modified_date"))
good = df.filter(~invalid)
w = Window.partitionBy("customer_id").orderBy(F.col("modified_date").desc())
dedup = good.withColumn("_rn", F.row_number().over(w)).filter(F.col("_rn")==1).drop("_rn")
bad.write.format("delta").mode("append").save(quarantine_path)

if DeltaTable.isDeltaTable(spark, silver_path):
    target = DeltaTable.forPath(spark, silver_path)
    (target.alias("t").merge(dedup.alias("s"), "t.customer_id=s.customer_id")
      .whenMatchedUpdateAll(condition="s.modified_date >= t.modified_date")
      .whenNotMatchedInsertAll().execute())
else:
    dedup.write.format("delta").mode("overwrite").save(silver_path)

print("Bronze rows:", df_bronze.count(), "Silver rows:", dedup.count(), "Quarantine rows:", bad.count())
