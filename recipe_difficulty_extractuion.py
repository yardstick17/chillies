# -*- coding: utf-8 -*-
import os
import re

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import struct
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

EASY_MAX_TIM = 30
MIN_HARD_TIME = 60


def time_in_minutes(time_in_string_format):
    minute_relation = [60, 1, 1.0 / 60]
    matches = re.findall('PT(\d*H)?(\d*M)?(\d*S)?', time_in_string_format)
    time = 0
    if matches:
        for given_time, relation in zip(matches[0], minute_relation):
            given_time = given_time[:-1]
            if given_time:
                time += (int(given_time) * relation)
    return time


def is_recipe_difficult(row):
    all_times = [time_in_minutes(time_in_string_format) for time_in_string_format in row]
    try:
        if sum(all_times) <= EASY_MAX_TIM:
            return 'Easy'
        elif sum(all_times) > MIN_HARD_TIME:
            return 'Hard'
        return 'Undefined'
    except:
        return 'Undefined'


if __name__ == '__main__':
    recipes_dir = 'recipes-etl'
    conf = SparkConf().setAppName('DifficultyColumnAdd')
    spark = SparkSession \
        .builder \
        .appName('IsRecipeDifficult') \
        .getOrCreate()

    df = spark.read.json('recipes.json')
    chiles_df = df.where(col('ingredients').like('%chilli%'))
    # chiles_varients = set(['chilies', 'chilly'])
    # chiles_df = df.select(df.columns).rdd.filter(lambda x: 'chilies' in str(x.ingredients)).toDF()
    # chiles_df = df.filter(lambda x: True if set(str(x.ingredients).split()) & chiles_varients else False)

    transform_to_difficulty = udf(
        lambda row: is_recipe_difficult(row),
        StringType())

    time_columns = ['prepTime', 'cookTime']
    chiles_df = chiles_df.withColumn('difficulty',
                                     transform_to_difficulty(struct([chiles_df[x] for x in time_columns])))

    chiles_df.write.parquet(os.path.join(recipes_dir, 'result'))