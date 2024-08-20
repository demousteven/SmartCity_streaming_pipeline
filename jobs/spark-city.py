# Import necessary modules from PySpark and other packages
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DoubleType

# Import configuration settings for accessing AWS credentials
from config import configuration

def main():
    # Initialize a Spark session with necessary configurations for Kafka and AWS S3 access
    spark = SparkSession.builder.appName("SmartCityStreaming") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY')) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY')) \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .getOrCreate()

    # Adjust the log level to minimize console output, focusing only on warnings and errors
    spark.sparkContext.setLogLevel('WARN')

    # Define the schema for the vehicle data received from Kafka
    vehicleSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("make", StringType(), True),
        StructField("model", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("fuelType", StringType(), True),
    ])

    # Define the schema for the GPS data
    gpsSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("vehicleType", StringType(), True)
    ])

    # Define the schema for the traffic data
    trafficSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("cameraId", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("snapshot", StringType(), True)
    ])

    # Define the schema for the weather data
    weatherSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("location", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("weatherCondition", StringType(), True),
        StructField("precipitation", DoubleType(), True),
        StructField("windSpeed", DoubleType(), True),
        StructField("humidity", IntegerType(), True),
        StructField("airQualityIndex", DoubleType(), True),
    ])

    # Define the schema for the emergency incident data
    emergencySchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("incidentId", StringType(), True),
        StructField("type", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("status", StringType(), True),
        StructField("description", StringType(), True),
    ])

    # Function to read data from a specified Kafka topic and parse it according to the given schema
    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')  # Specify Kafka as the data source
                .option('kafka.bootstrap.servers', 'broker:29092')  # Kafka broker address
                .option('subscribe', topic)  # Kafka topic to subscribe to
                .option('startingOffsets', 'earliest')  # Start reading from the earliest offset
                .load()
                .selectExpr('CAST(value AS STRING)')  # Convert the Kafka message value to a string
                .select(from_json(col('value'), schema).alias('data'))  # Parse the JSON string using the specified schema
                .select('data.*')  # Extract the fields from the parsed JSON
                .withWatermark('timestamp', '2 minutes')  # Add a watermark to handle late data
                )

    # Function to write streaming data to S3 in Parquet format, with checkpointing for fault tolerance
    def streamWriter(input: DataFrame, checkpointFolder, output):
        return (input.writeStream
                .format('parquet')  # Specify Parquet as the output format
                .option('checkpointLocation', checkpointFolder)  # Set the checkpoint location
                .option('path', output)  # Set the output path in S3
                .outputMode('append')  # Append new data to the existing dataset
                .start())

    # Read and process data streams from different Kafka topics using their respective schemas
    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema).alias('vehicle')
    gpsDF = read_kafka_topic('gps_data', gpsSchema).alias('gps')
    trafficDF = read_kafka_topic('traffic_data', trafficSchema).alias('traffic')
    weatherDF = read_kafka_topic('weather_data', weatherSchema).alias('weather')
    emergencyDF = read_kafka_topic('emergency_data', emergencySchema).alias('emergency')

    # Write the processed data streams to S3 in Parquet format with appropriate checkpointing
    query1 = streamWriter(vehicleDF, 's3a://spark-streaming-data/checkpoints/vehicle_data',
                          's3a://spark-streaming-data/data/vehicle_data')
    query2 = streamWriter(gpsDF, 's3a://spark-streaming-data/checkpoints/gps_data',
                          's3a://spark-streaming-data/data/gps_data')
    query3 = streamWriter(trafficDF, 's3a://spark-streaming-data/checkpoints/traffic_data',
                          's3a://spark-streaming-data/data/traffic_data')
    query4 = streamWriter(weatherDF, 's3a://spark-streaming-data/checkpoints/weather_data',
                          's3a://spark-streaming-data/data/weather_data')
    query5 = streamWriter(emergencyDF, 's3a://spark-streaming-data/checkpoints/emergency_data',
                          's3a://spark-streaming-data/data/emergency_data')

    # Wait for the streaming queries to terminate
    query5.awaitTermination()

if __name__ == "__main__":
    main()
