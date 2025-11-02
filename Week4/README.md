# ⚡ Real-Time Anime Data Analytics 

## 📌 Introduction
This project uses **Apache Spark Structured Streaming** to process and analyze **real-time JSON data** about anime series.  
The streaming data is continuously processed, stored into **PostgreSQL**, and visualized dynamically using **Power BI**.

**Objectives:**
1. Read real-time data from JSON files in the `data/` directory using **Apache Kafka** 
2. Process and clean the data using **Apache Spark**.  
3. Generate two analytical datasets:  
   - `op_per_year`: yearly statistics of anime.  
   - `op_rating`: summary of user ratings.  
4. Continuously write transformed data into **PostgreSQL**.  
5. Create real-time visual reports using **Power BI** dashboards.

---

## 🗂️ Directory Structure
```
Week4/
│
├── check_dir/
│   ├── commits/
│   ├── offsets/
│   ├── sources/
│   └── metadata/
│
├── data/
│   └── OnePiece.json                 # Real-time JSON input
│
├── kafka/
│   └── kafka_producer.py             # Kafka producer for streaming
│
├── report/
│   ├── op_dashboard.pbix             # Power BI dashboard
│   └── PSQL.sql                      # PostgreSQL table creation script
│
├── spark/
│   └── processing_data.ipynb         # Spark processing notebook
│
├── postgresql-42.7.3.jar             # PostgreSQL JDBC driver
├── .gitignore
└── README.md
```

---

## ⚙️ 1️⃣ Real-Time Data Streaming

### 📘 Description
- The project reads real-time anime data from **JSON files** using **Apache Kafka** (simulating live stream).  
- Each record includes details such as anime name, episode count, year, and rating.  
- Data is streamed to **Spark Structured Streaming** for continuous processing.

### 🧮 Spark Code Logic
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("RealTimeAnimeAnalytics") \
    .config("spark.jars", "postgresql-42.7.3.jar") \
    .getOrCreate()

df = spark.readStream \
    .schema(schema) \
    .json("data/")

# Processing logic
op_per_year = df.groupBy("year").agg(count("*").alias("anime_count"))
op_rating = df.groupBy("title").agg(avg("rating").alias("avg_rating"))
```

---

## 🧾 2️⃣ Data Storage in PostgreSQL

### 📘 Description
The processed data is **continuously written into PostgreSQL** using the **JDBC connector**.

### 🧮 Code Example
```python
op_per_year.writeStream \
    .foreachBatch(lambda batch, _: batch.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/anime_db") \
        .option("dbtable", "op_per_year") \
        .option("user", "postgres") \
        .option("password", "your_password") \
        .mode("append") \
        .save()) \
    .start()
```

### 🧱 Database Tables
- **op_per_year:** Yearly summary of anime releases.  
- **op_rating:** Average ratings per anime title.  

---

## 📊 3️⃣ Visualization with Power BI

### 📘 Description
- The **Power BI** dashboard (`op_dashboard.pbix`) connects directly to the **PostgreSQL** database.  
- It provides **real-time visual analytics** such as:
  - Total anime released per year.
  - Average rating trends.
  - Top-rated anime overview.
  - Rating distribution by genre.

---

## ⚙️ 4️⃣ Technologies Used
| Component | Description |
|------------|-------------|
| **Apache Spark** | Real-time data processing and transformation |
| **PostgreSQL** | Relational database for storing processed data |
| **Power BI** | Visualization and real-time reporting |
| **Python (Kafka, PySpark)** | Data ingestion and streaming pipeline |
| **JSON** | Input data format |

---

## 🚀 5️⃣ How to Run the Project

### 🧱 Prerequisites
- Python 3.12  
- Apache Spark 4.0+  
- PostgreSQL 15+  
- Power BI Desktop  
- `postgresql-42.7.3.jar` (JDBC Driver)

### 🧩 Steps
1. Place input JSON file into `data/` directory.  
2. Run Kafka producer:
   ```bash
   python kafka/kafka_producer.py
   ```
3. Open and run Spark notebook:
   ```bash
   spark/processing_data.ipynb
   ```
4. Check data in PostgreSQL:
   ```sql
   SELECT * FROM op_per_year;
   SELECT * FROM op_rating;
   ```
5. Open `report/op_dashboard.pbix` in **Power BI** to visualize.

---

## 📈 Summary
| Task | Output | Storage |
|------|---------|----------|
| Real-time JSON ingestion | Raw stream data | Spark |
| Yearly anime statistics | `op_per_year` | PostgreSQL |
| Average rating summary | `op_rating` | PostgreSQL |
| Dashboard visualization | Power BI | Live data view |

---

## 👨‍💻 Author
**Hải Hoàng**  
📅 Project: Week 4 – Real-Time Anime Data Analytics  
🧩 Environment: Python 3.12, Spark 4.0.1, PostgreSQL, Power BI, JSON Streaming  
