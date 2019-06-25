# webis-tldr-17-corpus
This repository contains code for constructing TLDR corpus from Reddit Corpus as described in [TL;DR: Mining Reddit to Learn Automatic Summarization, EMNLP 2017 - New Frontiers in Summarization workshop](https://aclanthology.info/papers/W17-4508/w17-4508)

## About this code

This code is intended to be run using Spark framework for working with large Reddit dumps directly. It consists of two scripts:

`make_reddit.py` - Reads the raw dumps and creates content-summary pairs in the form of Spark dataframe.

`clean_reddit.py` - Reads the result of the previous script and applies some normalization for improving precision of the final corpus.

The resources folder contains an exhaustive list of Reddit bots which we use to filter automatic postings.

## Usage

`spark-submit --master yarn make_tldr.py --input_comments input-comments-path --input_submissions input-submissions-path --output_comments tldr-comments-raw --output_submissions tldr-submissions-raw`

__We use Mistune library to remove markdown, which should be passed to Spark using `--py-files`__

`spark-submit --master yarn --py-files /usr/local/lib/python3.5/dist-packages/mistune.py clean_tldr.py --input_comments tldr-comments-raw --input_submissions tldr-submissions-raw --output_comments tldr-comments-cleaned --output_submissions tldr-submissions-cleaned`

## Released corpus

The current version of the corpus can be found here on [Zenodo](https://zenodo.org/record/1043504#.Wzt7PbhXryo)


## Script Descriptions
all of these steps are leveraging normal python funcntions though, called used spark, should be easy to port over to normal python

### clean_tldr.py

1. reads in as jsons:

```python
args = parser.parse_args()
input_comments = str(args.input_comments)
input_submissions = str(args.input_submissions)
output_comments = str(args.output_comments)
output_submissions = str(args.output_submissions)

comments_df = spark.read.json(input_comments)
submissions_df = spark.read.json(input_submissions)
print("Initial number of comments: {}".format(comments_df.count()))
print("Initial number of submissions: {}".format(submissions_df.count()))
```

2. clean text
- clean all the text fields
  - using clean_text
- remove special chars (line 66)

3. filter
- remove non english posts
  - using check_english
- filter if content_len <= summary len or summary_len=0

### make_tldr.py
reads in and out as jsons

1. Remove posts where body/selftext == '[deleted]' 
2. Remove posts by bots and deleted authors
3. Find posts containing any form of a tl.{0,3}dr pattern
4. Find posts containing only a single occurrence of such pattern
5. Find posts containing a valid pattern
6. Find the location of this pattern in a post and split the text into content-summary pair of appropriate lengths (content > summary)
