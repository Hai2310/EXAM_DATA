# 🧠 Anime Data Analytics using Apache Spark

## 📌 Introduction
This project uses **Apache Spark** to process and analyze data from two main sources:
- `animes.csv`: information about anime series.
- `ratings.csv`: user rating data.

**Objectives:**
1. Calculate the average and total number of ratings for each anime.
2. Analyze the number of ratings of different anime types by **user** and by **year**.
3. Compute the average rating of **users by genre**.
4. Compare the performance among **CSV**, **Parquet**, and **ORC** formats.
5. Save the results to **HDFS** with partitions by `year/month/day/hour`.

---

## 🗂️ Directory Structure
```
Week3/
│
├── data/ # Source data
│ ├── animes.csv
│ ├── ratings.csv
│ └── id_to_genreids.json
│
├── Spark/
│ ├── preprocess_data.ipynb # Main Spark data processing notebook
│ └── save_hdfs.ipynb # Notebook to save data to HDFS
│
├── output/
│ ├── csv/
│ │ └── animes_best_rated/
│ ├── evaluate/
│ │ ├── csv/
│ │ ├── orc/
│ │ └── parquet/
│ └── parquet/
│ ├── animes_best_rated/
│ ├── genres_user/
│ └── type_per_year/
│
└── README.md
```



## ⚙️ 1️⃣ Analysis #1 — Average and Total Ratings per Anime

### 📘 Description
- Read `ratings.csv` and `animes.csv`.
- Join both datasets by `anime_id`.
- Calculate:
  - `avg_rating` – average score of each anime.
  - `total_votes` – total number of ratings.

### 🧮 Spark Code Logic
```python
from pyspark.sql.functions import avg, count

ratings = spark.read.csv("data/ratings.csv", header=True, inferSchema=True)
animes = spark.read.csv("data/animes.csv", header=True, inferSchema=True)

animes_best_rated = (
    ratings.groupBy("anime_id")
    .agg(
        avg("rating").alias("avg_rating"),
        count("rating").alias("total_votes")
    )
    .join(animes, "anime_id")
)
```
📤 Output

Dataset: animes_best_rated

Output Path: /output/parquet/animes_best_rated/

Fields: anime_id, name, avg_rating, total_votes

## ⚙️ 2️⃣ Analysis #2 — Number of Ratings per Anime Type by User per Year
### 📘 Description

Combine rating data with anime genre/type information.

Extract year from the timestamp column.

Count the number of ratings by user, genre, and year.

### 🧮 Spark Code Logic
```
from pyspark.sql.functions import year, explode, col, count

genres_user = (
    ratings.withColumn("year", year("timestamp"))
    .join(animes.select("anime_id", "genres"), "anime_id")
    .withColumn("genre", explode(col("genres")))
    .groupBy("user_id", "year", "genre")
    .agg(count("*").alias("total_rated"))
)
```
### 📤 Output

Dataset: genres_user

Output Path: /output/parquet/genres_user/

Fields: user_id, year, genre, total_rated

## ⚙️ 3️⃣ Analysis #3 — Average User Rating by Genre
### 📘 Description

Each user may watch multiple genres → explode the genres column.

Calculate the average rating per user for each genre.

### 🧮 Spark Code Logic
```
from pyspark.sql.functions import avg, explode, col

type_per_year = (
    ratings.join(animes, "anime_id")
    .withColumn("genre", explode(col("genres")))
    .groupBy("user_id", "genre")
    .agg(avg("rating").alias("avg_rating"))
)
```
### 📤 Output

Dataset: type_per_year

Output Path: /output/parquet/type_per_year/

Fields: user_id, genre, avg_rating

## 🧾 4️⃣ Format Comparison: CSV vs Parquet vs ORC

### 🧪 Evaluation

The same dataset (animes_best_rated) is read and measured by:

File size

Read/write speed

Query performance (filter, groupBy)

Format	Read Speed	  File Size 	Schema Support	 Write Speed
CSV	    ❌ Slow	    🔺 Large	  ❌ No	          ⚠️ Slow
Parquet	✅ Fast	    ✅ Small	     ✅ Yes	         ✅ Very Fast
ORC	    ✅ Very Fast	✅ Smallest	 ✅ Yes	         ✅ Fast
➡️ Conclusion

Parquet is the most efficient format for large-scale data analytics in Spark due to its columnar storage and compression capabilities.

## 🗃️ 5️⃣ Saving Data to HDFS

### 🧱 HDFS Directory Structure
```
/user/hdfs/week4/
├── animes_best_rated/
├── genres_user/
└── type_per_year/
```
### 📘 Time-based Partitioning

When saving to HDFS, data is partitioned by:

year

month

day

hour

### 🧮 Example Code
```
animes_best_rated.write.mode("overwrite") \
    .partitionBy("year", "month", "day", "hour") \
    .parquet("hdfs://namenode:9000/user/hdfs/week4/animes_best_rated")

Same for Other Datasets
genres_user.write.mode("overwrite") \
    .partitionBy("year", "month", "day", "hour") \
    .parquet("hdfs://namenode:9000/user/hdfs/week4/genres_user")

type_per_year.write.mode("overwrite") \
    .partitionBy("year", "month", "day", "hour") \
    .parquet("hdfs://namenode:9000/user/hdfs/week4/type_per_year")
```
### 📈 Summary Table
```
Analysis	Objective	Dataset Output	HDFS Path
#1	Average & total ratings per anime	animes_best_rated	/week4/animes_best_rated
#2	Ratings by user & genre per year	genres_user	/week4/genres_user
#3	Average rating per user per genre	type_per_year	/week4/type_per_year
```
### 💡 Future Enhancements

Automate the pipeline using Spark Submit + Airflow

Add visualizations in Power BI or Tableau

Perform sentiment analysis on anime descriptions

### 👨‍💻 Author

Hoang Minh Hai
📅 Project: Week 3 – Anime Data Analysis with Apache Spark
🧩 Environment: Python 3.12, PySpark 4.0.1, HDFS, Parquet/ORC