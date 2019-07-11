#!/bin/python3.7
import sys
import requests
import json
from amadeus import Client, ResponseError
import time
API_KEY = open("key.env").read().strip()
print("Key", API_KEY)
API_SECRET = open("secret.env").read().strip()
print("Secret", API_SECRET)

start = time.time()
unformated_body = requests.get("http://ip-api.com/json").content.decode("utf-8")
body = json.loads(unformated_body)
lat = body["lat"]
long = body["lon"]

amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)
try:
    response = amadeus.reference_data.locations.airports.get(
        latitude=lat,
        longitude=long
    )
    print(response.data)
except ResponseError as e:
    print(e)
end = time.time()
print(end - start)
