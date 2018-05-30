#!/usr/bin/python
# -*- coding: utf-8 -*

# Geocoding addresses using the national address database API - https://adresse.data.gouv.fr/ - BAN 

import argparse
import sys
import requests
import json

def geocodage(address):
    try:
        r = requests.get('https://api-adresse.data.gouv.fr/search/?q='+address)
        global json_data
        json_data = json.loads(r.text)
        return json_data
    except:
        print("Error")

def reverse(lat, lon):
    try:
        r = requests.get('https://api-adresse.data.gouv.fr/reverse/?lon='+lon+'&lat='+lat)
        global json_data
        json_data = json.loads(r.text)
        return json_data
    except:
        print("Error")

def parse_geocodage(address):
    try:
        json_data = geocodage(address)
    except:
        print("Enable to geocode data...")
        sys.exit()
    try:
        adr = json_data["features"][0]["properties"]["label"]
        return(adr)
    except:
        print("error parsing data")

def parse_reverse(lat, lon):
    try:
        json_data = reverse(lat, lon)
    except:
        print("Enable to reverse data...")
        sys.exit()
    try:
        label = json_data["features"][0]["properties"]["label"]
        return label
    except:
        print("Parsing reverse error")

def csv(json_data):
    try:
        adr = json_data["features"][0]["properties"]["housenumber"]
        adr += ";"
    except:
        print("No housenumber!")
        adr = ""
    try:
        adr += json_data["features"][0]["properties"]["street"]
        adr += ";"
    except:
        print("No Street!")
        adr = ""
    try:
        adr += json_data["features"][0]["properties"]["postcode"]
        adr += ";"
        adr += json_data["features"][0]["properties"]["city"]
        adr += ";"
        # adr += str(json_data["features"][0]["properties"]["citycode"])
        # adr += ";"
        adr += gps(json_data)
        return(adr)
    except:
        print("error parsing data")

def gps(json_data):
    try:
        c_gps = str(json_data["features"][0]["geometry"]["coordinates"])
        c_gps = c_gps.replace("[","").replace("]","")
        return(c_gps)
    except:
        print("error parsing coordinates")

def score(json_data):
    try:
        score = json_data["features"][0]["properties"]["score"]
        return (score)
    except:
        print("error parsing coordinates")

def version():
    print ("hello, i'm in version one")

parser = argparse.ArgumentParser(description="Geocoding addresses using the national address database API - https://adresse.data.gouv.fr/ - BAN \nThe data come from IGN, La Poste, DGFiP, Etalab and OpenStreetMap France.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-a", "--address", type=str, help="enter the address to geocoder")
parser2 = parser.add_argument_group()
parser2.add_argument("--lat", "--latitude", type=str, help="enter Latitude")
parser2.add_argument("--lon", "--longitude", type=str, help="enter Longitude")
parser.add_argument("-s", "--score", action="store_true", default=False, help="show score")
parser.add_argument("-g", "--gps", action='store_true', default=False, help="show coordinates")
parser.add_argument("--csv", action='store_true', default=False, help="show all in csv format")
parser.add_argument("--version", action="store_true", default=False, help="show version")

args = parser.parse_args()

# print(args) # affichage du dictionnaire pour mise au point

if len(sys.argv) == 1:
    print("Specify arguments. Pass --help or -h to display help")
    sys.exit()
if args.version:
    version()
    sys.exit()
if args.address:
    print(parse_geocodage(args.address))
if (args.lat and not args.lon) or (args.lon and not args.lat):
    print("Please indicate latitude and longitude, not just one of them.")
    sys.exit()
if args.lat and args.lon:
    print(parse_reverse(args.lat, args.lon))
if json_data["features"] == []:
    print("Exiting...")
    sys.exit()
if args.gps:
    print("Coordinates :",gps(json_data))
if args.score:
    print("Score :", score(json_data))
if args.csv:
    print(csv(json_data))
