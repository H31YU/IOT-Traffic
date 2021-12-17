import gzip
import json
import requests
import ast

#response = requests.get(response = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/3772",params={"key":"5c61c92e-77b3-4269-a62a-cf87ad1e1d54"}))
response = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist",params={"key":""})
response= ast.literal_eval(response.text)
with open("metsites.json", "w") as write_file:
    json.dump(response, write_file, indent=4)


print("Done writing PrettyPrinted JSON data into file with indent=4")