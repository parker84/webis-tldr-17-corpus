
select 
    tldr_summary
    ,len_tldr_summary
    ,selftext
    ,is_bot
    ,author
    ,num_tldrs
from reddit_posts
limit 10;


drop table if exists filtered_reddit_posts;
create table filtered_reddit_posts as
select * 
from reddit_posts
where
    -- len_tldr_summary <= len_tldr_content and
    tldr_summary is not null and
    len_tldr_summary > 0 and
    -- (selftext != '[deleted]' or
    -- body != '[deleted]') and
    selftext != '[deleted]' and
    is_bot = false and
    is_english is not null and
    author is not null and
    num_tldrs = 1;


select 
    tldr_summary
    ,len_tldr_summary
    ,selftext
    ,is_bot
    ,author
    ,num_tldrs
from filtered_reddit_posts
limit 10;