
# depth-first toteutus paketin läpikäyjälle.
# Tämän kirjoitin alkuun vain todistaakseni itselleni miten lista-tuple
# -rakenteen rekursiivinen läpikäynti toimii, mutta tämä on ihan hyödyllinen
# koska tarkistaa samalla datan olevan perusmuotoisesti oikein. Ei-merkkijono
# avaimet ja ei-kaksi kokoiset tuplet aiheuttavat Exceptionin.
def pkt_recurse(obj, depth=0):
  # jos objekti on lista, se koostuu n:stä avain-arvo parista.
  # kys. avain-arvo -parit ovat tupleja.
  if isinstance(obj, list):
    for i in range(len(obj)):
      pkt_recurse(obj[i], depth+1)

  # jos objekti on tuple, se on avain-arvo pari. Avain on aina string,
  # arvo voi olla lista jos objekti jatkuu "syvemmälle", tai jokin primitiivinen
  # arvo jos objektin "syvyys" loppuu tähän.
  if isinstance(obj, tuple):
    key, value = obj

    if not isinstance(key, str) or len(obj) != 2:
      raise Exception("Datassa jotain pielessa.")

    # jos arvo oli lista, täytyy jatkaa syvemmälle.
    if isinstance(value, list):
      pkt_recurse(value, depth+1)
      value = pkt_stringOrType(value)
    
    print(depth*"-" + f"{key}: {value}")


# apufunktio, palauttaa parametrinsa sellaiesnaan jos se oli merkkijono,
# muussa tapauksessa parametrinsa tyypin.
def pkt_stringOrType(obj):
  return obj if isinstance(obj, str) else type(obj)


# yleinen rule-preserv. -matchaava funktio. Käy rekursiivisesti läpi
# koko rakenteen, ja testaa sääntöä kaikkia avain-arvo -pareja vastaan
# (myös ei-primitiivi arvoja, näissä arvona tyyppi). Jos sääntö palauttaa
# True, edes yhdestä, palautetaan True. Tämä on tarkoitettu apupalikaksi muiden funktioiden
# rakennusta helpottamaan, ei tarvitse kopioida rekursiokoodia turhaan niin
# pysyy paketti vähän paremmin kasassa.
def pkt_objRulePreservation(obj, rule):
  returnValue = False

  if isinstance(obj, list):
    for i in range(len(obj)):
      recursReturn = pkt_objRulePreservation(obj[i], rule)
      if recursReturn:
        returnValue = True

  if isinstance(obj, tuple):
    key, value = obj

    if isinstance(value, list):
      recursReturn = pkt_objRulePreservation(value, rule)
      if recursReturn:
        returnValue = True
      value = pkt_stringOrType(value)

    if rule(key, value):
      returnValue = True 

  return returnValue



# palauttaa True tai False sen perusteella kuuluuko paketti säilyttää vai ei.
# Jos paketti sisältää avaimena ainakin yhden avainlistan avaimista, palautetaan
# True. Muuten false. Tarkoitettu käytettäväksi paketit läpi  looppaavan funktion
# "apupalikkana".
def pkt_preserveKeysAny(obj, matchList):
  def rule(key, value):
    return key in matchList
  return pkt_objRulePreservation(obj, rule)



# kuin pkt_preserveKeysAny, mutta tässä riittää että match listasta löytyy jokin, joka
# on edes substring jotain avainta. Esimerkiksi jos avaimena löytyy http2.header, niin
# match lista ["htt"] riittää säilyttämään paketin.
# Huom. string on itsensä substring, joten tämä on aina löysempi filtteri kuin tarkkaan 
# matchaava.
def pkt_preserveKeysAnySubstr(obj, matchList):
  def rule(key, value):
    for candidate in matchList:
      if candidate in key:
        return True
    return False
  
  return pkt_objRulePreservation(obj, rule)


# Kuin pkt_preserveKeysAny, mutta KAIKKIEN listassa olevien avainten täytyy löytyä paketista.
def pkt_preserveKeysAll(obj, matchList):
  for matchable in matchList:
    if not pkt_preserveKeysAny(obj, [matchable]):
      return False
  return True

# kuin pkt_preserveKeysAnySubstr, mutta KAIKKIEN listassa olevien avainten täytyy löytyä 
#  substrineinä paketin avaimista.
def pkt_preserveKeysAllSubstr(obj, matchList):
  for matchable in matchList:
    if not pkt_preserveKeysAnySubstr(obj, [matchable]):
      return False
  return True



# Tämä säilyttää paketin, jos siltä löytyy __mistä vain__ substringinä jokin sille
# annetuista tekstinpätkistä. Siis mistä vain tarkoittaen, että matchaaminen
# suoritetaan sekä avaimia että arvoja vastaan, ja kumpikin kelpaa "validoimaan
# säilyttämisen".
def pkt_preserveSubstr(obj, matchList):
  def rule(key, value):
    if not isinstance(value, str):
      value = ""
    for matchable in matchList:
      if matchable in key or matchable in value:
        return True
    return False
  return pkt_objRulePreservation(obj, rule)


# kuin pkt_preserveSubstr, mutta KAIKKIEN mainittujen tulee löytyä substringinä
# sen sijaan että yhden mainitun löytyminen riittäisi.
def pkt_preserveSubstrAll(obj, matchList):
  for matchable in matchList:
    if not pkt_preserveSubstr(obj, [matchable]):
      return False
  return True



# Ottaa listan listoja. Jokaisesta listasta täytyy löytyä ainakin yksi matchi
# paketin headereista, jotta säilytetään.
def pkt_preserveEachSublistExactMatch(obj, matchList):
  for matchable in matchList:
    if not pkt_preserveKeysAny(obj, matchable):
      return False
  return True



# Tämä funktio toteuttaa luonnollisen kielen lauseen
# ""Palauta paketilta kaikkien näiden avainten avain-arvo parit"".
# avain-arvo parit ovat tupleina, arvo palautetaan as-is vaikka se
# ei olisikaan primitiivinen.
# Tämä toteutus ohittaa mahdollisesti löytymättömät avaimet nostamatta niistä
# Exceptionia
def pkt_keyValuesByKeys(obj, keyList):
  returnList = []

  if isinstance(obj, list):
    for i in range(len(obj)):
      recursReturn = pkt_keyValuesByKeys(obj[i], keyList)
      returnList.extend(recursReturn)

  if isinstance(obj, tuple):
    key, value = obj

    if isinstance(value, list):
      recursReturn = pkt_keyValuesByKeys(value, keyList)
      returnList.extend(recursReturn)

    if key in keyList:
      returnList.append(obj)

  return returnList



# tämä funktio toteuttaa luonnollisen kielen lauseen 
# "“palauta objektilta avain-arvo parit, joista löytyy joku annetuista avainsanoista
# vähintään substringinä avaimesta tai arvosta”.

def pkt_keyValuesBySubstr(obj, keyList):
  returnList = []

  if isinstance(obj, list):
    for i in range(len(obj)):
      recursReturn = pkt_keyValuesBySubstr(obj[i], keyList)
      returnList.extend(recursReturn)

  if isinstance(obj, tuple):
    key, value = obj

    if isinstance(value, list):
      recursReturn = pkt_keyValuesBySubstr(value, keyList)
      returnList.extend(recursReturn)

    if not isinstance(value, str):
      value = ""

    for matchable in keyList:
      if matchable in key or matchable in value:
        returnList.append(obj)

  return returnList












