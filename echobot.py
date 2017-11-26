import requests, xmltodict, json

xml = requests.get('http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=mhide')
dict = xmltodict.parse(r.content)
json = json.dumps(o)
