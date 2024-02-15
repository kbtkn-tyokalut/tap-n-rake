from readjson import *
from parserengine import *


"""
käytettävissä olevat palikat

## Filtteröintifunktiot
- pkt_preserveKeysAny(obj, matchList)
- pkt_preserveKeysAnySubstr(obj, matchList)
- pkt_preserveKeysAll(obj, matchList)
- pkt_preserveKeysAllSubstr(obj, matchList)
- pkt_preserveSubstr(obj, matchList)
- pkt_preserveSubstrAll(obj, matchList)

## Arvojennoutofunktiot
- pkt_keyValuesByKeys(obj, keyList)
- pkt_keyValuesBySubstr(obj, keyList)

"""

requestPath = ["http.request.uri", "http2.headers.path"]
requestFullURI = ["http.request.full_uri", "http2.request.full_uri"]
responseURI = ["http.response_for.uri"] # ei HTTP/2 -vastinetta


# sievennysfunktio, näyttää ei-mjonot tyyppeinä
# olettaa saavansa listan tupleja
def pkt_prettify_keyvals(listOfTuples):
  for printable in listOfTuples:
    key, value = printable
    if not isinstance(value, str):
      value = type(value)
    print(f"{key}: {value}")

# sievennysfunktio, mutta yksittäisille arvoille avain-arvo
# parien sijaan.
def pkt_prettify_uniqs(listOfValues):
  for printable in listOfValues:
    print(printable)


##
## request path components
##
def getRequestPaths():
  return pkt_keyValuesByKeys(pkt_data, requestPath)

def showRequestPaths():
  pkt_prettify_keyvals(getRequestPaths())

def getUniqRequestPaths():
  uniqs = set()
  allRequestPaths = getRequestPaths()
  for requestPath in allRequestPaths:
    uniqs.add(requestPath[1])
  return list(uniqs)

def showUniqRequestPaths():
  pkt_prettify_uniqs(getUniqRequestPaths())





