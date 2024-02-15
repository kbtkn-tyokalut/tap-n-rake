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




def lpqm_printDomains(obj):
  sortedDomains = sorted(obj, key=lambda x: len(x), reverse=True)
  print("no.\tEndpoints\tDomain")
  for i in range(len(sortedDomains)):
    print(f"{i}.\t{len(sortedDomains[i])-1}\t{sortedDomains[i][0]}")


# domain nimi tai järjestysnumero
def lpqm_printPathsByDomain(data, domain):
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
  
  paths = []
  for i in range(1, len(obj)):
    paths.append([obj[i][1], obj[i][0]])
  paths.sort(key=lambda x: x[1])

  for index, path in enumerate(paths):
    print(f"{index}\t{path[0]}: {path[1]}")




