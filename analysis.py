from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import col
from pyspark.sql import functions as f
from pyspark.sql.functions import monotonically_increasing_id

# 数据读取
spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df = spark.read.format("csv").option("header", "true").load("Python_jobs_cleaned.csv")
df.printSchema()
df.show(5)
# 公司招聘信息数量统计
df.groupby("companyShortName").count().orderBy(col("count").desc()).show()
# 公司规模统计
df.groupby("companySize").count().orderBy(col("count").desc()).show()
# 公司融资情况统计
df.groupby("financeStage").count().orderBy(col("count").desc()).show()
# 城市招聘信息数量统计
df.groupby("city").count().orderBy(col("count").desc()).show()
# 地区招聘信息数量统计
df.groupby("district").count().orderBy(col("count").desc()).show()
# Python相关职位招聘数量统计
df.groupby("positionName").count().orderBy(col("count").desc()).show()
# 学历要求统计
df.groupby("workYear").count().orderBy(col("count").desc()).show()
# 工作经验要求统计
df.groupby("education").count().orderBy(col("count").desc()).show()
# 平均月薪统计
df1 = df.select("salary_min", f.translate(f.col("salary_min"), "k", "").alias("salary_min1"))
df1 = df1.withColumn("salary_min1", df1["salary_min1"].cast("Int"))
df2 = df.select("salary_max", f.translate(f.col("salary_max"), "k", "").alias("salary_max1"))
df2 = df2.withColumn("salary_max1", df2["salary_max1"].cast("Int"))
df1 = df1.withColumn("id", monotonically_increasing_id())
df2 = df2.withColumn("id", monotonically_increasing_id())
df3 = df1.join(df2, df1.id == df2.id)
df4 = df3.withColumn('salary_average', (df3.salary_min1 + df3.salary_max1) / 2) \
    .select('salary_min1', 'salary_max1', 'salary_average')
df4.groupby("salary_average").count().orderBy(col("count").desc()).show()
# 公司经营范围统计
df.groupby("industryField").count().orderBy(col("count").desc()).show()
# 岗位类型统计
df.groupby("firstType").count().orderBy(col("count").desc()).show()
df.groupby("secondType").count().orderBy(col("count").desc()).show()
