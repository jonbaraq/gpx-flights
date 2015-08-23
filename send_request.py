import json
import logging
import urllib2

data = { "request": {
    "slice": [
      {
        "origin": "ZRH",
        "destination": "MAD",
        "date": "2015-08-20",
        "maxStops": 0
      },
      {
        "origin": "MAD",
        "destination": "ZRH",
        "date": "2015-08-24",
        "maxStops": 0
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 10,
    # "refundable": false
  }
}

url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=xyz"
jsonreq = json.dumps(data, encoding = 'utf-8')
req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
flight = urllib2.urlopen(req)
response = flight.read()
flight.close()
print(response)
