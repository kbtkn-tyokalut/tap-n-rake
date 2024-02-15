import json


pkt_fileName = input("File to be read in: ")

if pkt_fileName == "":
  pkt_fileName = "example_com/example_com.json"

pkt_fileName = "pakettidata/" + pkt_fileName

pkt_fileHandle = open(pkt_fileName, "r")
pkt_data = json.load(pkt_fileHandle, object_pairs_hook=lambda x: x)
