from decimal import Decimal
from math import pow

import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DecimalType, ArrayType
from pyspark.sql.functions import udf, explode


def calc_periodic_value(value, coupon, yyield, type, duration):
    sList = []

    if type == "A":
        type_val = 1
    elif type == "S":
        type_val = 2
    elif type == "Q":
        type_val = 4
    elif type == "M":
        type_val = 12
    else:
        type_val = 0

    c = value * ((coupon*100)/type_val)
    tpv = Decimal(0)

    for x in range(duration):
        aList = []

        if (x+1) == duration:
            pv = (Decimal(value) / Decimal(pow(1 + ((yyield*100)/type_val), Decimal(x+1)))) + \
                 (Decimal(c) / Decimal(pow(1 + ((yyield*100)/type_val), Decimal(x+1))))
            tpv += pv
            aList.append(x+1)
            aList.append(c)
            aList.append(pv)
            aList.append(tpv)
            aList.append(tpv/value)
        else:
            pv = Decimal(c) / Decimal(pow(1 + ((yyield*100)/type_val), Decimal(x+1)))
            tpv += pv
            aList.append(x+1)
            aList.append(c)
            aList.append(pv)
            aList.append(Decimal(0))
            aList.append(Decimal(0))

        sList.append(aList)

    return sList


spark = SparkSession \
    .builder \
    .master('local') \
    .appName("bonds") \
    .getOrCreate()

in_file = os.path.join(os.path.dirname(os.path.realpath('__file__')), '..', 'bonds.json')

input_schema = StructType([StructField("id", StringType(), True),
                           StructField("value", StringType(), True),
                           StructField("coupon", StringType(), True),
                           StructField("yield", StringType(), True),
                           StructField("type", StringType(), True),
                           StructField("duration", StringType(), True)])

in_df = spark.read.schema(input_schema).json(in_file)

in_cast_df = in_df.filter("id!='null'").select(
                                  in_df.id,
                                  in_df.value.cast(DecimalType()),
                                  in_df.coupon.cast(DecimalType(10, 5)),
                                  in_df['yield'].cast(DecimalType(10, 5)),
                                  in_df.type,
                                  in_df.duration.cast(IntegerType()))

in_cast_df.show()

periodic_value_schema = StructType([StructField("period", IntegerType(), True),
                                    StructField("cp", DecimalType(12, 5), True),
                                    StructField("pv", DecimalType(12, 5), True),
                                    StructField("aggpv", DecimalType(12, 5), True),
                                    StructField("quote", DecimalType(12, 5), True)])

udf_calc_periodic_value = udf(calc_periodic_value, ArrayType(periodic_value_schema))

in_cast_df.withColumn("periodic_value", udf_calc_periodic_value(in_cast_df["value"], in_cast_df["coupon"],
                                                                in_cast_df["yield"], in_cast_df["type"],
                                                                in_cast_df["duration"]))\
    .withColumn("periodic_value", explode("periodic_value"))\
    .select("id", "value", "periodic_value.period", "periodic_value.cp", "periodic_value.pv", "periodic_value.aggpv",
            "periodic_value.quote")\
    .createOrReplaceTempView("periodic_value_table")

spark.sql("select id as `Bond ID`, period as `Period`, cp as `Coupon payment`, pv as `PV of periodic payments`, "
          "aggpv as A from periodic_value_table").show(50)

spark.sql("select id as `Bond ID`, aggpv as A, value as `FV`, quote as `Quote` "
          "from periodic_value_table where NOT aggpv = '0.00000'").show()

spark.stop()
