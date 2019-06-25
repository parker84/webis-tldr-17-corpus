import sys
import argparse
import unicodedata
from pyspark import SparkContext,SparkConf,SQLContext
from pyspark.sql import Row,SparkSession,HiveContext
from pyspark.sql.functions import col,size,explode,split
from pyspark.sql.types import StringType,IntegerType,ArrayType
from pyspark.sql.functions import udf, array, length
from bs4 import BeautifulSoup
import mistune
import re
from nltk.corpus import stopwords
from data.tldr.clean_tldr_helpers import clean_text, check_english

spark = SparkSession.builder.appName("webis-tldr-17-corpus-normalization").getOrCreate()
sc = spark.sparkContext
print(sc)
print(spark)

parser = argparse.ArgumentParser(description="Clean the summarization corpus constructed from make_reddit")
parser.add_argument('--input_comments', type=str, help="HDFS path to Reddit comments")
parser.add_argument('--input_submissions', type=str, help="HDFS path to Reddit submissions")
parser.add_argument('--output_comments', type=str, help="HDFS path to save processed comments")
parser.add_argument('--output_submissions', type=str, help="HDFS path to save processed submissions")

args = parser.parse_args()
input_comments = str(args.input_comments)
input_submissions = str(args.input_submissions)
output_comments = str(args.output_comments)
output_submissions = str(args.output_submissions)

comments_df = spark.read.json(input_comments)
submissions_df = spark.read.json(input_submissions)
print("Initial number of comments: {}".format(comments_df.count()))
print("Initial number of submissions: {}".format(submissions_df.count()))

cleanText = udf(clean_text, StringType())
checkEnglish = udf(check_english, StringType())
removeSpecialCharsContent = udf(lambda input: re.sub(r"\W+$", "", str(input)).strip(), StringType())
removeSpecialCharsSummary = udf(lambda input: re.sub(r"^\W+","",str(input)).strip(), StringType())
length_udf = udf(lambda input:len(input.strip().split()), IntegerType())


comments_df = comments_df.withColumn('content',checkEnglish(comments_df.content))
submissions_df = submissions_df.withColumn('content', checkEnglish(submissions_df.content))
comments_df = comments_df.filter(comments_df.content.isNotNull())
submissions_df = submissions_df.filter(submissions_df.content.isNotNull())
print("After removing  non-english posts -> comments: {}".format(comments_df.count()))
print("After removing  non-english posts -> submissions : {}".format(submissions_df.count()))

comments_df = comments_df.withColumn('normalized_body',cleanText(comments_df.body))
comments_df = comments_df.withColumn('normalized_content',cleanText(comments_df.content))
comments_df = comments_df.withColumn('normalized_summary',cleanText(comments_df.summary))

submissions_df = submissions_df.withColumn('normalized_selftext', cleanText(submissions_df.selftext))
submissions_df = submissions_df.withColumn('normalized_content', cleanText(submissions_df.content))
submissions_df = submissions_df.withColumn('normalized_summary', cleanText(submissions_df.summary))

comments_df = comments_df.withColumn('normalized_content', removeSpecialCharsContent(comments_df.normalized_content))
submissions_df = submissions_df.withColumn('normalized_content', removeSpecialCharsContent(submissions_df.normalized_content))
comments_df = comments_df.withColumn('normalized_summary', removeSpecialCharsSummary(comments_df.normalized_summary))
submissions_df = submissions_df.withColumn('normalized_summary', removeSpecialCharsSummary(submissions_df.normalized_summary))

comments_df = comments_df.withColumn('content_len',length_udf(comments_df.normalized_content))
comments_df = comments_df.withColumn('summary_len',length_udf(comments_df.normalized_summary))
comments_df = comments_df.withColumn('body_len',length_udf(comments_df.normalized_body))

submissions_df = submissions_df.withColumn('content_len', length_udf(submissions_df.normalized_content))
submissions_df = submissions_df.withColumn('summary_len', length_udf(submissions_df.normalized_summary))
submissions_df = submissions_df.withColumn('selftext_len', length_udf(submissions_df.normalized_selftext))

comments_df = comments_df.where(comments_df['content_len']>comments_df['summary_len'])
submissions_df = submissions_df.where(submissions_df['content_len']>submissions_df['summary_len'])
comments_df = comments_df.where(comments_df['summary_len']>0)
submissions_df = submissions_df.where(submissions_df['summary_len']>0)


print("Saving cleaned comments to {}".format(output_comments))
comments_df.write.json(output_comments)
print("Done")
print("Saving cleaned submissions to {}".format(output_submissions))
submissions_df.write.json(output_submissions)
print("Done")



