import os
import csv
import requests

HOST = os.environ["DATABRICKS_HOST"]
TOKEN = os.environ["DATABRICKS_TOKEN"]
WAREHOUSE_ID = os.environ["DATABRICKS_WAREHOUSE_ID"]

SQL = "SELECT * FROM gym_dashboard.gym.silver_gym"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "statement": SQL,
    "warehouse_id": WAREHOUSE_ID
}

resp = requests.post(
    f"{HOST}/api/2.0/sql/statements",
    headers=headers,
    json=payload
)
resp.raise_for_status()

statement_id = resp.json()["statement_id"]

# Poll until finished
while True:
    status = requests.get(
        f"{HOST}/api/2.0/sql/statements/{statement_id}",
        headers=headers
    ).json()

    if status["status"]["state"] == "SUCCEEDED":
        break

# Extract results
columns = [c["name"] for c in status["manifest"]["schema"]["columns"]]
rows = status["result"]["data_array"]

os.makedirs("out", exist_ok=True)
csv_path = "out/gym_silver.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"CSV written to {csv_path}")
