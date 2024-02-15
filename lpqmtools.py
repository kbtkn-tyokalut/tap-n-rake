from urllib.parse import urlparse, parse_qs

def addIntoLPQMStructure(obj, method, parsed_url):
  domain = parsed_url.netloc
  path = parsed_url.path
  qstring = parse_qs(parsed_url.query)
  #print(f"{method}, {domain}, {path}, {qstring}")

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
            print(f"HUOM! Monta metodia samaan endpointtiin! {subObj[1]}, {method}, {subObj[0]}")
          #yhdistetään qstring objektit
          subObj[2].update(qstring)
      if not pathExisted:
        domainObject.append([path, method, qstring])
  if not domainExisted:
    obj.append([domain, [path, method, qstring]])
  obj.sort(key=lambda x: len(x), reverse=True)




def lpqm_printDomains(obj):
  print("no.\tEndpoints\tDomain")
  for i in range(len(obj)):
    print(f"{i}.\t{len(obj[i])-1}\t{obj[i][0]}")


# domain nimi tai järjestysnumero
def lpqm_printPathsByDomain(data, domain):
  # obj:iin otetaan se yksi käsiteltävä objekti jonka domaini matchaa
  obj = []
  if isinstance(domain, int):
    obj = data[domain]
  else:
    for dom in data:
      if dom[0] == domain:
        obj = dom
        break
    else:
      print("Tarkista domainin nimi")
      return
  
  print(obj[0])

  paths = []
  for i in range(1, len(obj)):
    paths.append([obj[i][1], obj[i][0]])
  paths.sort(key=lambda x: x[1])

  for index, path in enumerate(paths):
    print(f"{index}\t{path[0]}: {path[1]}")


# matchList voi olla merkkijono tai se voi olla lista merkkijonoja.
# poistetaan objekti, jos sen domaini ei mätchää mitään merkkijonoa vasten.
def lpqm_deleteNonMatchingDomains(obj, matchList):
  keepables = []
  if isinstance(matchList, str):
    matchList = [matchList]
  for domain in obj:
    domainName = domain[0]
    keep = False
    for matchable in matchList:
      if matchable in domainName:
        keep = True
    if keep:
      keepables.append(domain)
  obj.clear()
  obj.extend(keepables)



def lpqm_printQStrings(obj):
  
  for domainObj in obj:
    print(f"####  {domainObj[0]}  ####")
    for i in range(1, len(domainObj)):
      print(f"> {domainObj[i][1]}: {domainObj[i][0]}")
      for key, value in domainObj[i][2].items():
        print(f">>> {key}: {value}")
    print()


def lpqm_getQStringsRaw(obj):
  returnList = []
  for domainObj in obj:
    for i in range(1, len(domainObj)):
      for key, value in domainObj[i][2].items():
        returnList.append((key, value))
  return returnList


def lpqm_getQStringsRawKeys(obj):
  returnList = []
  for domainObj in obj:
    for i in range(1, len(domainObj)):
      for key, value in domainObj[i][2].items():
        returnList.append(key)
  return returnList
