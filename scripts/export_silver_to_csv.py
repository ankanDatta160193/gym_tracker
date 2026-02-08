import os
import pandas as pd
from databricks import sql

os.makedirs("exports", exist_ok=True)

conn = sql.connect(
    server_hostname=os.environ["DATABRICKS_HOST"].replace("https://", ""),
    http_path=f"/sql/1.0/warehouses/{os.environ['DATABRICKS_WAREHOUSE_ID']}",
    access_token=os.environ["DATABRICKS_TOKEN"]
)

query = "SELECT * FROM silver_gym"

df = pd.read_sql(query, conn)
df.to_csv("exports/gym_silver.csv", index=False)

conn.close()
print("CSV written to exports/gym_silver.csv")
