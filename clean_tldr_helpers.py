import sys
import argparse
import unicodedata
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import mistune

# To avoid recursion depth errors when using Mistune library for removing markdown
sys.setrecursionlimit(300000)
global markdownParser
markdownParser = mistune.Markdown()
global stop
stop = set(stopwords.words("english"))
stop.update(['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me','my' 'him', 'her', 'us', 'them'])


def clean_text(input):
    input = re.sub(r'http\S+','',str(input))
    input = re.sub(r'https?:\/\/.*[\r\n]*', '', input, flags=re.MULTILINE)
    input = re.sub(r'&amp;', '', input)
    input = re.sub(r'[_"\;%()|+&=*%:#$@\[\]/]', '', input)
    input = re.sub('\.\.+', '.', input)
    input = re.sub('\!\!+', '!', input)
    input = re.sub('\?\?+', '?', input)
    input = re.sub('\-\-+', '-', input)
    parsed_text = ' '.join(BeautifulSoup(markdownParser(input),"lxml").findAll(text=True)).strip()
    clean_text = unicodedata.normalize("NFKD", parsed_text)
    return clean_text

def check_english(input):
    words = input.lower().split()[0:10]
    if stop.intersection(words):
        return input
    else:
        return None