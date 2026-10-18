# Databricks / PySpark example: Silver -> Gold.
from pyspark.sql import functions as F
storage_account = "<storage-account>"
customer_path = f"abfss://silver@{storage_account}.dfs.core.windows.net/banking/customer/"
account_path = f"abfss://silver@{storage_account}.dfs.core.windows.net/banking/account/"
txn_path = f"abfss://silver@{storage_account}.dfs.core.windows.net/banking/transaction/"
gold_customer360 = f"abfss://gold@{storage_account}.dfs.core.windows.net/customer_360/"
gold_monthly_txn = f"abfss://gold@{storage_account}.dfs.core.windows.net/monthly_transactions/"

customers = spark.read.format("delta").load(customer_path)
accounts = spark.read.format("delta").load(account_path)
transactions = spark.read.format("delta").load(txn_path)
account_summary = accounts.groupBy("customer_id").agg(
 F.countDistinct("account_id").alias("account_count"),
 F.sum("balance").alias("total_account_balance"))
customer_360 = customers.join(account_summary,"customer_id","left").fillna(
 {"account_count":0,"total_account_balance":0.0})
monthly = (transactions.withColumn("transaction_month",F.date_trunc("month",F.col("transaction_date")))
 .groupBy("transaction_month","account_id")
 .agg(F.count("*").alias("transaction_count"),F.sum("amount").alias("net_transaction_amount")))
customer_360.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(gold_customer360)
monthly.write.format("delta").mode("overwrite").option("overwriteSchema","true").save(gold_monthly_txn)
print("Silver customer keys:",customers.select("customer_id").distinct().count())
print("Gold customer_360 keys:",customer_360.select("customer_id").distinct().count())
