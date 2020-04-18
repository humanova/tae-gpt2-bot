import pandas as pd
import sys
import csv 
import codecs

def conv(file):
    with codecs.open(file, 'r', encoding="utf-8") as f:
        comment_data = f.readlines()

    with codecs.open(f"{file}.csv", 'w', encoding="utf-8") as f:
      wr = csv.writer(f)
      wr.writerow(("comment"))
      wr.writerows(comment_data)
    f.close()

def convert(file):
    comment_data = []
    with codecs.open(file, 'r', encoding="utf-8") as f:
        for l in f.readlines():
            comment_data.append(l.replace("\n", ""))

    df = pd.DataFrame(comment_data)
    df.to_csv(f"{file}.csv", index=False)
    

if __name__ == "__main__":
    convert(sys.argv[1])
    #conv(sys.argv[1])