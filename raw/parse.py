import re
from glob import glob
import json

files = glob("www*regionalsprache*de/phonD2/0aa*.html")

all_data = []
for file in files:    
    with open(file) as f:
        text = f.read()
        h2 = re.findall('<h2 class="unnumbered"><strong><i>(.*?)</i></strong>',
                    text)[0]
        data = re.findall(r'"data":\[\[.*?\]\]', text)
        if data:
            data = json.loads("{"+data[0]+"}")
            data = data["data"]
            print(h2, len(data))
            for i in range(len(data[0])):
                row = [h2]
                for j in range(10):
                    row += [data[j][i]]
                all_data += [row]
                
languages = []
with open("data.tsv", "w") as f:
    f.write("\t".join([
        "Concept",
        "LID",
        "WNUM",
        "LName",
        "Sampa",
        "Tokens",
        "CV",
        "Classes",
        "Sonority",
        "Type",
        "Filename"])+"\n")
    for row in all_data:
        lnum, lname = re.findall("'([^']*).html'>([^<]*)<", row[2])[0]
        row.insert(1, lnum)
        row[3] = lname
        
        f.write("\t".join([str(c) for c in row])+"\n")

