import os
import pandas as pd
from databricks import sql

HOST = os.environ["DATABRICKS_HOST"]
TOKEN = os.environ["DATABRICKS_TOKEN"]
WAREHOUSE_ID = os.environ["DATABRICKS_WAREHOUSE_ID"]

OUTPUT_PATH = "exports/gym_silver.csv"

conn = sql.connect(
    server_hostname=HOST.replace("https://", ""),
    http_path=f"/sql/1.0/warehouses/{WAREHOUSE_ID}",
    access_token=TOKEN,
)

query = "SELECT * FROM silver_gym"

df = pd.read_sql(query, conn)
os.makedirs("exports", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"CSV written to {OUTPUT_PATH}")
