#!/usr/bin/python
# -*- coding: utf-8 -*

import json
import sys
import urllib.parse

import click
import requests


def geocodage(verbose, address):
    try:
        if verbose:
            print("[+] Geocoding address...")
        address = urllib.parse.quote(address)
        r = requests.get('https://api-adresse.data.gouv.fr/search/?q=' + address)
        json_data = json.loads(r.text)
        results = []
        if json_data is not None:
            i = 0
            for _ in json_data["features"]:
                tmp = {"address": json_data["features"][i]["properties"]["label"],
                       "score": json_data["features"][i]["properties"]["score"],
                       "latitude": json_data["features"][i]["geometry"]["coordinates"][0],
                       "longitude": json_data["features"][i]["geometry"]["coordinates"][1]}
                # results.append(json_data["features"][i]["properties"]["label"])
                data = str(tmp["address"]) + ";" + str(tmp["score"]) + ";" + str(tmp["latitude"]) + ";" + str(
                    tmp["longitude"])
                results.append(data)
                i = i + 1
        return results
    except:
        print("Error")


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help="Verbose mode")
@click.option('--address', '-a', help='Address to be geocoded', required=True, type=str)
@click.option('--nb', '-n', help='Number of results to return  [default=1]', default=0, show_default=False, type=int)
@click.option('--gps', is_flag=True, help='Show only GPS coordinates')
def cli(verbose, address, nb, gps):
    if verbose:
        print("Geocoding addresses using the national address database API - https://adresse.data.gouv.fr/ - BAN")
    address = geocodage(verbose, address)
    if address is not None:
        nbresults = len(address)
        i = 0
        if nb!=0:
            nb = nb - 1
        for _ in address:
            if gps:
                if verbose:
                    print("{:10} {:10}".format("Longitude", "Latitude"))
                print("{:10} {:10}".format(address[i].split(";")[3], address[i].split(";")[2]))
            if not gps:
                if verbose:
                    print("{:10} {:10} {:18} {:10}".format("Longitude", "Latitude", "Score", "Address"))

                    print("{:10} {:10} {:10} {:10}".format(address[i].split(";")[3], address[i].split(";")[2],
                                                           address[i].split(";")[1], address[i].split(";")[0]))
                    if nb == nbresults:
                        pass
                    elif nb > nbresults:
                        nb = nbresults
                    elif nb == i:
                        break
                    else:
                        pass
                    i = i + 1


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cli.main(['--help'])
    else:
        cli()
