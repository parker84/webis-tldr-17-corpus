import itertools
import csv
import re
from settings import BOT_LIST_PATH

global botlist
with open(BOT_LIST_PATH,'r') as bot_file:
    reader=csv.reader(bot_file)
    botlist=list(reader)
botlist = list(itertools.chain.from_iterable(botlist))

# Check for presence of a tldr pattern
def tl_dr(input):
    lower_text = str(input).lower()
    match = re.search(r'tl.{0,3}dr',str(lower_text))
    if match:
        return input
    else:
        return None

# Find all the matched tldr patterns
def get_all_tldr(input):
    lower = str(input).lower()
    pattern=re.compile(r'tl.{0,3}dr') 
    return pattern.findall(lower)

# Find location of the tldr pattern and split text to form <content, summary> pairs
def iter_tldr(text):
    lower_text = str(text).lower()
    patterns = re.findall(r'tl.{0,3}dr',lower_text)
    if len(patterns) > 0:
        match = patterns[-1]
        if match:
            index = lower_text.rfind(match)
            if index == 0 or index+len(match) == len(str(lower_text)):
                return None
            else:
                content = text[:index].strip()
                summary = text[index+len(match):].strip()
                if len(content.split()) > len(summary.split()):
                    return [content,summary]
                else:
                    return None
        else:
            return None
    else:
        return None