# Gym Data Pipeline  
**Databricks (Community) · Delta Lake · GitHub Actions · Google Sheets**

This project implements a fully automated, end-to-end gym activity data pipeline using only free-tier tools. The objective is to ingest workout data, structure it properly, and expose it for analysis with zero manual effort.

---

## Design Goals

- Free-tier compatible  
- Fully automated and reproducible  
- Simple architecture with minimal moving parts  
- Easy to debug and extend  

---

## High-Level Architecture

The pipeline follows a **medallion architecture**:

- **Bronze Layer**  
  Raw attendance and workout logs with minimal transformation.

- **Silver Layer**  
  Structured, exploded, analytics-ready data at set-level granularity.

- **Export Layer**  
  CSV snapshot committed to GitHub for downstream consumption.

---

## Data Flow

1. Workout and attendance data is ingested into Bronze Delta tables  
2. A single Databricks notebook transforms Bronze → Silver  
3. Workout sets are exploded into one row per set  
4. Reps, weights, and volume metrics are calculated  
5. GitHub Actions triggers the notebook and waits for completion  
6. Silver data is exported as a CSV and committed to the repo  
7. Google Sheets reads the CSV directly from GitHub  

---

## Bronze Layer

Stores raw, append-only data with minimal cleanup.

### Tables

- `attendance_bronze` – daily gym attendance logs  
- `gym_workouts_bronze` – raw workout entries  

Data is stored in **Delta format**. Overwrites are used since volume is small and reprocessing is acceptable.

---

## Silver Layer

Contains analytics-ready, structured data.

### Key Transformations

- Date normalization  
- Exercise and muscle group standardization  
- Explosion of sets into row-level records  
- Alignment of reps and weights  
- Exercise volume calculation  

### Important Columns

- `date`  
- `exercise`  
- `set_no`  
- `reps`  
- `set_weight`  
- `exercise_volume`  

Set-level granularity is intentionally stored in Silver to avoid reprocessing raw data later.

---

## Databricks Notebook

All transformations are implemented in **one notebook**:

- Reads Bronze tables  
- Applies deterministic transformations  
- Overwrites Silver Delta table  

This avoids orchestration complexity in Databricks Community Edition.

---

## GitHub Actions Automation

GitHub Actions acts as the orchestrator.

### Workflow Steps

1. Trigger Databricks notebook via REST API  
2. Poll until execution completes  
3. Export Silver table as CSV  
4. Commit and push the file  

The workflow explicitly waits for Databricks to finish to avoid exporting stale data.

---

## CSV Export
The Silver table is exported to the following location in the repository:
`exports/gym_silver.csv`

# Export Behavior

- The file is overwritten on every successful run

- Commits are skipped automatically if the exported data has not changed

- The CSV always represents the latest successful pipeline run

- No historical files are retained to keep the repository clean

- This design ensures downstream consumers always read a single, stable snapshot.

3 Google Sheets Integration

Google Sheets consumes the exported CSV directly from GitHub using:

`=IMPORTDATA("https://raw.githubusercontent.com/<username>/<repo>/main/exports/gym_silver.csv")`


- Sheets refresh automatically, enabling near real-time dashboards without requiring paid BI tools.

## Why This Design

- No paid services required

- No dependency on Databricks Jobs UI

- Deterministic and easy to debug

- Clear separation of concerns

- Easy to extend into a Gold layer later

# Future Improvements

- Gold aggregation tables (weekly volume, PR tracking)

- Slowly changing dimensions for exercises

- Data quality checks

- API-based ingestion instead of CSV exports

- Author Notes

# Built as a personal data engineering project to demonstrate:

- Medallion architecture

- Spark transformations

- Free-tier orchestration

- End-to-end automation
