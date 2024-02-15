from readjson import *
from parserengine import *
from urllib.parse import urlparse, parse_qs
from lpqmtools import *

"""
käytettävissä olevat palikat

## Filtteröintifunktiot
- pkt_preserveKeysAny(obj, matchList)
- pkt_preserveKeysAnySubstr(obj, matchList)
- pkt_preserveKeysAll(obj, matchList)
- pkt_preserveKeysAllSubstr(obj, matchList)
- pkt_preserveSubstr(obj, matchList)
- pkt_preserveSubstrAll(obj, matchList)
- pkt_preserveEachSublistExactMatch(obj, matchList):

## Arvojennoutofunktiot
- pkt_keyValuesByKeys(obj, keyList)
- pkt_keyValuesBySubstr(obj, keyList)

"""

requestPath = ["http.request.uri", "http2.headers.path"]
requestFullURI = ["http.request.full_uri", "http2.request.full_uri"]
responseURI = ["http.response_for.uri"] # ei HTTP/2 -vastinetta

methods = ["http.request.method", "http2.headers.method"]


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



#
#  Full URI extraction
#
def getRequestURIs():
  return pkt_keyValuesByKeys(pkt_data, requestFullURI)



#
# Full URI + methods
#
def getMethodsAndURIs():
  returnList = []
  URIsAndMethods = requestFullURI + methods

  for packet in pkt_data:
    if pkt_preserveKeysAny(packet, requestFullURI): # tämä riittää, koska integriteettitarkistukset
      returnList.append(pkt_keyValuesByKeys(packet, requestFullURI+methods))
  return returnList



def getLocsPathsQueriesMethods():
  methodsAndURIs = getMethodsAndURIs()
  
  finalDataStructure = []

  #methods and URIs on lista listoja, jokainen ensimmäisen tason alilista vastaa yhtä pakettia.
  for packet in methodsAndURIs:
    #if len(packet) != 2:
      #raise Exception("täysparsinnassa jotain hämärää")
      # note to self: http2:ssa joskus ilmeisesti on monta resurssipyyntöä yhdessä.

    
    tStruct1 = packet[0]
    tStruct2 = packet[1]

    if not tStruct1[0] in methods:
      print("järjestyspoikkeus")
      tStruct1, tStruct2 = tStruct2, tStruct1

    # tStruct1 on nyt varmuudella metodi ja 2 uri
    method = tStruct1[1]
    fullUri = tStruct2[1]

    parsed_url = urlparse(fullUri)

    addIntoLPQMStructure(finalDataStructure, method, parsed_url)
  return finalDataStructure

'''
def addIntoLPQMStructure(obj, method, parsed_url):
  domain = parsed_url.netloc
  path = parsed_url.path
  qstring = parse_qs(parsed_url.query)
  print(f"{method}, {domain}, {path}, {qstring}")
  
  domainExisted = False
  # jokaiselle domainilla oma sublista
  for domainObject in obj:
    # domainobjekti oli jo olemassa, lisätään sinne
    if domainObject[0] == domain:
      domainExisted = True
      pathExisted = False
      # [domain, [polku1, metodi1, qparams1], [...]]
      # käydään läpi kaikki jatko-objektit
      for subObjectIndex in range(1, len(domainObject)):
        subObj = domainObject[subObjectIndex]
        # jos polku oli jo olemassa, niin...
        if subObj[0] == path:
          pathExisted = True
          # ... huomautetaan, jos metodit eivät täsmää
          if subObj[1] != method:
            print("HUOM! Monta metodia samaan entpointtiin!")
          #yhdistetään qstring objektit
          subObj[2].update(qstring)
      if not pathExisted:
        domainObject.append([path, method, qstring])
  if not domainExisted:
    obj.append([domain, [path, method, qstring]])
'''

















#
# dataintegriteetin ja toimintalogiikan oikeellisuuden automaattiset tarkistus-
# funktiot.
requestFullURI, methods
def ensureFullURIsHaveMethods():
  for packet in pkt_data:
    foundFullURI = pkt_preserveKeysAny(packet, requestFullURI)
    foundMethods = pkt_preserveKeysAny(packet, methods)
    if foundFullURI and not foundMethods:
      raise Exception("Full-URI match ilman methodia. ")

automatic_tests = [
  ensureFullURIsHaveMethods
]

for test in automatic_tests:
  test()

