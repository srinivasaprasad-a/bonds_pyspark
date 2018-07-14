from decimal import Decimal
from math import pow

import os
import json

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DecimalType

# global vars
sList = []
sIndex = 0


def calc_periodic_value(_dfrow):
    if _dfrow.type == "A":
        type_val = 1
    elif _dfrow.type == "S":
        type_val = 2
    elif _dfrow.type == "Q":
        type_val = 4
    elif _dfrow.type == "M":
        type_val = 12
    else:
        type_val = 0

    c = _dfrow.value * ((_dfrow.coupon*100)/type_val)
    tpv = Decimal(0)

    for x in range(_dfrow.duration):
        aList = []

        if (x+1) == _dfrow.duration:
            pv = (Decimal(_dfrow.value) / Decimal(pow(1 + ((_dfrow['yield']*100)/type_val), Decimal(x+1)))) + \
                 (Decimal(c) / Decimal(pow(1 + ((_dfrow['yield']*100)/type_val), Decimal(x+1))))
        else:
            pv = Decimal(c) / Decimal(pow(1 + ((_dfrow['yield']*100)/type_val), Decimal(x+1)))

        tpv += pv

        aList.append(_dfrow.id)
        aList.append(x+1)
        aList.append(float(c))
        aList.append(float(pv))
        aList.append(float(tpv))

        sList.append(aList)

    return sList


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def create_periodic_value_table(dfrow):
    print type(dfrow)

    global sIndex
    sIndex = sIndex + 1

    calc_periodic_value(dfrow)

    if sIndex == in_cast_df_count:
        print sList

        """
        pvt_schema = StructType([StructField("id", StringType(), True),
                                 StructField("period", IntegerType(), True),
                                 StructField("cp", DecimalType(10, 5), True),
                                 StructField("pv", DecimalType(10, 5), True),
                                 StructField("aggpv", DecimalType(10, 5), True)])

        pvt_df = spark.createDataFrame(sList, pvt_schema)
        pvt_df.printSchema()
        pvt_df.show()
        """


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

# in_cast_df.printSchema()
in_cast_df.show()
in_cast_df_count = in_cast_df.count()
in_cast_df.foreach(create_periodic_value_table)

spark.stop()
