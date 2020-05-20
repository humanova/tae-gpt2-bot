# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
import json
import codecs
import pandas as pd
import sys

if __name__ == "__main__":
    f_name = sys.argv[1]
    with codecs.open(f_name, "r", "utf-8") as f:
        data = json.load(f)
    
    comments = []
    for c in data:
        comments.append(c["text"].strip().replace("\n", "<bs>"))
    
    df = pd.DataFrame(comments)
    df.to_csv(f"{f_name}.csv", index=False)