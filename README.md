# 🌦️ Weather ETL Pipeline  
### End‑to‑End Extract • Transform • Load Project (Python + Pandas + SQLite)

This project demonstrates a complete, production‑style ETL pipeline built in Python.  
It extracts hourly weather data from a public API, transforms it into analytics‑ready tables, and loads it into a SQLite database for downstream analysis.

The goal of this project is to showcase practical data engineering skills, including:

- API extraction  
- Data cleaning and feature engineering  
- Building a modular ETL architecture  
- Loading structured data into a relational database  
- Designing transformations that reflect real business logic  

---

## 🚀 Project Overview

This pipeline retrieves **48 hours of hourly weather data**, performs a series of transformations to enrich and clean the dataset, and stores the final result in a SQLite database.

The project is structured using a clear, industry‑standard ETL layout:
src/ extract/ transform/ load/

      ┌────────────┐
      │   Extract   │
      │  (API Call) │
      └──────┬─────┘
             │ Raw JSON
             ▼
      ┌────────────┐
      │ Transform   │
      │ Pandas ETL  │
      └──────┬─────┘
             │ Cleaned DataFrame
             ▼
      ┌────────────┐
      │    Load     │
      │  SQLite DB  │
      └────────────┘


---

## 📥 Extract Layer

The extract step calls a weather API and retrieves:

- Hourly temperature  
- Humidity  
- Wind speed & direction  
- Pressure  
- Visibility  
- Precipitation  
- Soil metrics  
- And more  

The raw response is stored in memory as a nested JSON structure.

---

## 🔧 Transform Layer

The transform step uses **pandas** to convert the messy API response into a clean, tabular dataset.

### Key transformations include:

#### **Data Cleaning**
- Timestamp parsing and timezone normalization  
- Rounding numeric fields  
- Handling missing values  

#### **Feature Engineering**
- Rolling temperature averages  
- Rolling humidity averages  
- Temperature deltas  
- Day vs night classification  
- “Feels colder/warmer” flags  
- Wind direction mapping (N, NE, E, etc.)  
- Wind risk index  
- Precipitation flags (rain/snow)  
- Comfort index  
- Visibility normalization  

These transformations mirror the kind of business logic used in analytics and forecasting.

---

## 🗄️ Load Layer

The final cleaned DataFrame is loaded into a **SQLite database** using Python’s `sqlite3` module.

- Creates the database if it doesn’t exist  
- Creates or replaces the target table  
- Loads all rows in a single operation  

The resulting database can be opened directly in **DB Browser for SQLite**.

---

## 📊 Example Use Cases

Once loaded, the dataset can support:

- Weather dashboards  
- Forecasting models  
- Risk scoring  
- Operational reporting  
- Exploratory analysis  

This project is designed to be extended — additional tables, aggregations, or downstream tools can be added easily.

---

## 🏗️ How to Run the Pipeline

### **Manual Execution**

You can run each stage individually:
uv run -m src.extract.api uv run -m src.transform.transform uv run -m src.load.loader


Or run the full pipeline via:
uv run python src/main.py


---

## 🕒 Automated Scheduling (Batch File + Windows Task Scheduler)

This project includes instructions for running the ETL pipeline automatically on a schedule — similar to how production pipelines operate.

### **1. Create a batch file**

Create a file named `run_weather_pipeline.bat`:
cd C:\Utilities\Repos\Weather-ETL uv run python src\main.py


- `cd` ensures the script runs from the correct working directory  
- `uv run` automatically uses the project’s virtual environment  
- No manual activation of `.venv` is required  

### **2. Schedule it with Windows Task Scheduler**

1. Open **Task Scheduler**  
2. Select **Create Basic Task**  
3. Name it (e.g., “Weather ETL Pipeline”)  
4. Choose a trigger (e.g., **Daily at 02:00**)  
5. Action → **Start a Program**  
6. Program/script:  
C:\path\to\run_weather_pipeline.bat


7. Finish and save  

Your ETL pipeline will now run automatically every day.

This mirrors the scheduling approach used in real data engineering environments.

---

## 🧪 Future Enhancements

- Add unit tests for transformation logic  
- Add daily and weekly aggregated tables  
- Add a scheduler (cron, Airflow, or Prefect)  
- Build a small dashboard (Streamlit or Power BI)  
- Add logging and error handling  

---

## 🎯 Purpose of This Project

This ETL pipeline was built to demonstrate:

- Clean, modular Python engineering  
- Real‑world data transformation skills  
- Ability to design and implement an end‑to‑end data workflow  
- Understanding of analytics‑ready data modeling  

It’s intentionally structured to reflect the expectations of data engineering teams.

---

## ⚠️ Note on Environment Choices

I’m aware that SQLite and DB Browser are not typical enterprise‑grade solutions.  
This project was developed on a work laptop during quiet periods, which limited the tools I could install.

On my personal machine, I would normally use:

- PostgreSQL  
- A `.env` file for secrets  
- A containerized environment (Docker)  

For this demonstration, I chose a simple and effective setup to focus on showcasing my ability to design, build, and maintain a complete ETL pipeline from start to finish.

---

**Marcus Richardson**