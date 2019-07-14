#!/home/erastos/projects/travel/cli/venv/bin/python
import sys
import requests
import json
from amadeus import Client, ResponseError
import argparse
import datetime
import csv

# Parse Args
parser = argparse.ArgumentParser(prog="Traveller", description="Flight Planner Application")
parser.add_argument("dest", action="store", help="The Destination Airport")
parser.add_argument("dest_date", action="store", help="Date of Arrival at Destination",
                    type=datetime.date.fromisoformat)

args = parser.parse_args()

# Get Airport Codes
airport_csv = open("airports.csv")
airport_csv = csv.reader(airport_csv)
airport_processed = {}
for row in airport_csv:
    if not row[13]:
        airport_processed[row[1]] = row[3]
    else:
        airport_processed[row[13]] = row[3]
# Amadeus Login
API_KEY = open("key.env").read().strip()
print(API_KEY)
API_SECRET = open("secret.env").read().strip()
print(API_SECRET)

# Get Lat and Long
unformated_body = requests.get("http://ip-api.com/json").content.decode("utf-8")
body = json.loads(unformated_body)
lat = body["lat"]
long = body["lon"]

try:
    # Get IATA Codes from Airport
    amadeus = Client(
        client_id=API_KEY,
        client_secret=API_SECRET
    )
    # Get Closest Airports
    response = amadeus.reference_data.locations.airports.get(
        latitude=lat,
        longitude=long
    )
    iata = [element["iataCode"] for element in response.data]

    # Get Flights from those airports
    t_n = 1
    for code in iata[:1]:
        flights = amadeus.shopping.flight_offers.get(
            origin=code,
            destination=args.dest,
            departureDate=args.dest_date,
            max=3
        )
        body = json.loads(flights.body)
        for trip in flights.data:
            output = "{0}:".format(t_n)
            for flight in trip["offerItems"][0]["services"][0]["segments"]:
                iata_code = flight["flightSegment"]["departure"]["iataCode"]
                output += " {0} ({1}) --->".format(iata_code, body["dictionaries"]["locations"][iata_code]["detailedName"])
            arrival = flight["flightSegment"]["arrival"]["iataCode"]
            output += " {0} ({1})".format(arrival, body["dictionaries"]["locations"][arrival]["detailedName"])
            print(output)
            t_n += 1
except ResponseError as e:
    print(e)
    sys.exit(1)
