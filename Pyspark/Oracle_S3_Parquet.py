import sys
import os
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark import *
import s3_snowflake as utils
spark = SparkSession.builder.master("local").appName("testing").getOrCreate()

ora_url=sys.argv[1]
oracle_user = sys.argv[2]
oracle_password=sys.argv[3]
# JO_TABLE_NAHICHAIYE=sys.argv[4] #if condition lga ke kr sakte unhe neglect

qry = "(select table_name FROM tabs) t"

ora_tmp = spark.read.format("jdbc").option("url", ora_url).option("user", oracle_user).option \
        ("password", oracle_password).option("dbtable", qry).option("driver", "oracle.jdbc.OracleDriver").load()

tabs=[x[0] for x in ora_tmp.collect()]

#reading tables
for x in tabs:
    print("importing data from"+x)
    # reading tables
    df=spark.read.format("jdbc").option("url",ora_url).option("user",oracle_user) \
    .option("password",oracle_password).option("dbtable",x) \
    .option("driver","oracle.jdbc.driver.OracleDriver").load()
# s3buctemp/customer/custome_120220
    # writing the tables into S3 as parquet format
    y= str(current_timestamp())
    file_path= 's3://s3bucketemp/' + x + '/' + x + y
   
    table=x
    path = "x + '/' + x + y"
    utils.s3_snowflake(path)
    df.write.parquet(file_path)
    # df.write.partitionBy("Year","Month").parquet("s3a://location")
