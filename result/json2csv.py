import json
import csv
from datetime import datetime

json_path = "./result/dataname/xxxx.json"   # put the path to the json file here
csv_path = "./result/test/xxxx.csv"    # the path of the output file goes here



# read json file
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# save as csv
with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # header
    writer.writerow(["username", "event", "event_detail", "content", "label"])
    
    for item in data:
        writer.writerow([
            item.get("speaker", ""),
            "text",
            "",
            item.get("utt", "").replace("\n", " ").strip(),
            item.get("category", "")
        ])

print(f"complete: {csv_path}")
