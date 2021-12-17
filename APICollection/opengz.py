import gzip
import json


with gzip.open("weather_14.json.gz", 'r') as fin:
    data = json.loads(fin.read().decode('utf-8'))

with open("weather_14.json", "w") as write_file:
    json.dump(data, write_file, indent=4)


print("Done writing PrettyPrinted JSON data into file with indent=4")