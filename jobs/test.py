from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("Test PySpark") \
        .getOrCreate()

    print("PySpark is working!")
    spark.stop()


if __name__ == "__main__":
    main()
