# -*- coding: utf-8 -*-
import os
import re

EASY_MAX_TIM = 30
MIN_HARD_TIME = 60
EASY = 'Easy'
HARD = 'Hard'
UNDEFINED = 'Undefined'


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
    try:

        all_times = [time_in_minutes(time_in_string_format) for time_in_string_format in row]
        if not any(all_times):
            return UNDEFINED
        if sum(all_times) <= EASY_MAX_TIM:
            return EASY
        elif sum(all_times) > MIN_HARD_TIME:
            return HARD
        return UNDEFINED
    except:
        return UNDEFINED


if __name__ == '__main__':
    from pyspark import SparkConf
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
    from pyspark.sql.functions import struct
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType

    recipes_dir = './recipes-etl'

    conf = SparkConf().setAppName('DifficultyColumnAdd')
    spark = SparkSession \
        .builder \
        .appName('IsRecipeDifficult') \
        .getOrCreate()

    # The file is in the hadoop file system.
    # Place this file using: hadoop fs -put recipes.json /recipes.json
    df = spark.read.json('recipes.json')
    chiles_df = df.where(col('ingredients').like('%chilli%'))

    transform_to_difficulty = udf(
        lambda row: is_recipe_difficult(row),
        StringType())

    time_columns = ['prepTime', 'cookTime']
    chiles_df = chiles_df.withColumn('difficulty',
                                     transform_to_difficulty(struct([chiles_df[x] for x in time_columns])))

    chiles_df.write.parquet(os.path.join(recipes_dir, 'result'))
