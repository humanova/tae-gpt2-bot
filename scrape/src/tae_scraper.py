# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
from scraper import CommentScraper
import codecs
import json 

MIN_CHAR_COUNT = 25
SUBREDDIT = "tamamahbapengelli"

word_filters = [
    "/untard",
    "/engelsiz",
    "/engel",
    "/un",
    "[sil",
    "[removed]",
    "[silindi]",
    "u/vreddit",
    "r/vreddit"
    "sans",
    "admin",
    "abece",
    "http",
    "masterpiece"]

if __name__ == "__main__":
    s = CommentScraper(SUBREDDIT, 10000)
    data = s.get_comments()
    
    final_comments = []
    for c in data:
        if not len(c['text']) < MIN_CHAR_COUNT:
            if not any(word.lower() in c['text'].lower() for word in word_filters):
                final_comments.append(c)

    with codecs.open(f"comments_{SUBREDDIT}.json", "w", "utf-8") as json_file:
        json.dump(final_comments, json_file, ensure_ascii=False)

    print(f"comment count : {len(final_comments)}")