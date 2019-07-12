#!/bin/python3.7
import sys
import requests
import json
from amadeus import Client, ResponseError
import argparse
import datetime

# Parse Args
parser = argparse.ArgumentParser(prog="Traveller", description="Flight Planner Application")
parser.add_argument("dest", action="store", help="The Destination Airport")
parser.add_argument("dest_date", action="store", help="Date of Arrival at Destination",
                    type=datetime.date.fromisoformat)

args = parser.parse_args()

# Amadeus Login
API_KEY = open("key.env").read().strip()
print("Key", API_KEY)
API_SECRET = open("secret.env").read().strip()
print("Secret", API_SECRET)

# Get Lat and Long
unformated_body = requests.get("http://ip-api.com/json").content.decode("utf-8")
body = json.loads(unformated_body)
lat = body["lat"]
long = body["lon"]

# Get IATA Codes from Airport
amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)
try:
    # Get Closest Aiports
    response = amadeus.reference_data.locations.airports.get(
        latitude=lat,
        longitude=long
    )
    iata = [element["iataCode"] for element in response.data]

    # Get Flights from those airports
    for code in iata[:2]:
        flights = amadeus.shopping.flight_offers.get(
            origin=code,
            destination=args.dest,
            departureDate=args.dest_date
        )
        print(flights.data)
except ResponseError as e:
    print(e)
    sys.exit(1)
