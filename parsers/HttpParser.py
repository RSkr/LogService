import logging
import datetime
import re
import os
import pprint
import glob
import pandas as pd
from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import regexp_extract
from pyspark.sql.functions import col
from pyspark.sql.functions import sum as spark_sum
from pyspark.sql.functions import udf
from pyspark.sql import functions as F

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3"
java8_location = '/usr/lib/jvm/java-8-oracle'  # Set your own
os.environ['JAVA_HOME'] = java8_location

sc = SparkContext()
sc.setLogLevel(logLevel="ERROR")
sqlContext = SQLContext(sc)
spark = SparkSession(sc)

class HttpParser:
    def __init__(self, filepath, range_days, test_mode=False):
        self.status_code = 404
        self.amount_to_list = 10
        self.logs_df = []
        self.logs_df_len = 0
        self.status_freq_df =[]
        self.status_freq_df_len = 0
        self.status_404 = 0

        self.testMode = test_mode
        self.filepath = filepath
        if range_days is not None:
            self.fromDate = datetime.datetime.today() - datetime.timedelta(days=range_days)
            self.dateTime = datetime.datetime.strftime(self.fromDate,"%d/%b/%Y:%H:%M:%S")
        else:
            self.fromDate = None
        self.parse()

    # Parse File
    def parse(self):
        
        base_df = spark.read.text(self.filepath)
        
        host_pattern = r'(^\S+\.[\S+\.]+\S+)\s'
        ts_pattern = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})]'
        method_uri_protocol_pattern = r'\"(\S+)\s(\S+)\s*(\S*)\"'
        status_pattern = r'\s(\d{3})\s'
        content_size_pattern = r'\s(?:\d{3})\s(\d+).*$'
        self.logs_df = base_df.select(regexp_extract('value', host_pattern, 1).alias('host'),
                        regexp_extract('value', ts_pattern, 1).alias('timestamp'),
                        regexp_extract('value', method_uri_protocol_pattern, 1).alias('method'),
                        regexp_extract('value', method_uri_protocol_pattern, 2).alias('endpoint'),
                        regexp_extract('value', method_uri_protocol_pattern, 3).alias('protocol'),
                        regexp_extract('value', status_pattern, 1).cast('integer').alias('status'),
                        regexp_extract('value', content_size_pattern, 1).cast('integer').alias('content_size'))
        if self.fromDate is not None:
            self.logs_df = self.logs_df.filter(self.logs_df["timestamp"]  > self.dateTime).cache()


        self.status_freq_df = (self.logs_df
            .groupBy('status')
            .count()
            .sort('status')
            .cache())
        
        not_found_df = self.logs_df.filter(self.logs_df["status"] == self.status_code).cache()  
        
        status_404_df = self.logs_df.filter(self.logs_df["status"] == 404).cache()
        self.status_404 = status_404_df.count()
        
        endpoints_statusCode_count_df = (not_found_df
            .groupBy("endpoint")
            .count()
            .sort("count", ascending=False)
            .limit(self.amount_to_list))

        
        hosts_statusCode_count_df = (not_found_df
            .groupBy("host")
            .count()
            .sort("count", ascending=False)
            .limit(self.amount_to_list))
        
        self.logs_df_len = self.logs_df.count()
        self.status_freq_df_len = self.status_freq_df.count()
        if not self.testMode:
            print("------------------HTTP---------------------")
            print("Total file lines:\n" + str(self.logs_df.count()))
            print("-----------------------")
            print("Total distinct HTTP Status Codes:\n" + str(self.status_freq_df.count()))
            print("-----------------------")
            print("Status Codes table:")
            self.status_freq_df.show()
            print("-----------------------")
            print(('Total ' + str(self.status_code) + ' responses: {}').format(not_found_df.count()))  
            
            print("-----------------------")

            print('Top' + str(self.amount_to_list) + ' ' + str(self.status_code) + ' Response Code Endpoints:\n')
            endpoints_statusCode_count_df.show(truncate=False)
            print("-----------------------")

            print('Top' + str(self.amount_to_list) + ' ' + str(self.status_code) +  ' Response Code Hosts:\n')
            hosts_statusCode_count_df.show(truncate=False)
            print("--------------END of HTTP-------------------")
        return 0

    def getLogs(self):
        return {'lines': self.logs_df_len,
                 'codes': self.status_freq_df_len,
                 'statusError' : self.status_404
                        }