import json
import urllib.parse

import pandas as pd
import requests

from .addresses_matcher import AddressesMatcher


def perform_geocoding(address, limit, verbose):
    """
    Perform geocoding for a given address using an external geocoding API.

    Parameters:
    - address (str): The address to geocode.
    - limit (int): The maximum number of results to return.
    - verbose (bool): Flag to enable verbose output.

    Returns:
    - geocoded (DataFrame): A pandas DataFrame containing geocoded results,
      including coordinates and address labels.
    """
    if verbose:
        print("[+] Geocoding address : {}".format(address))
    address = urllib.parse.quote(address)
    r = requests.get('https://api-adresse.data.gouv.fr/search/?q=' + address)
    if len(r.text) != 136 and r.status_code == 200:
        json_data = json.loads(r.text)
        df = pd.json_normalize(
            json_data['features'],
            sep='_',
            record_path=None,
            meta=[
                'type',
                ['properties', 'label'],
                ['properties', 'score'],
                ['properties', 'housenumber'],
                ['properties', 'id'],
                ['properties', 'name'],
                ['properties', 'postcode'],
                ['properties', 'citycode'],
                ['properties', 'x'],
                ['properties', 'y'],
                ['properties', 'city'],
                ['properties', 'context'],
                ['properties', 'type'],
                ['properties', 'importance'],
                ['properties', 'street'],
                'geometry.type',
                ['geometry', 'coordinates']
            ],
            errors='ignore'
        )

        # Assuming 'geocoded' is a pandas DataFrame and 'geometry_coordinates' contains pairs like [lon, lat]
        if 'geometry_coordinates' in df.columns:
            # Reverse the order of each pair [lon, lat] -> [lat, lon]
            df['geometry_coordinates'] = df['geometry_coordinates'].apply(
                lambda coords: [coords[1], coords[0]] if isinstance(coords, list) and len(coords) == 2 else coords)

        geocoded = df.loc[:limit].copy()
        return geocoded
    else:
        return None


def local_geocoding(input_file, database, processes, verbose):
    """
    Perform local geocoding on a set of addresses using a local Base Adresse Nationale (BAN) database.

    This function reads a file containing addresses, geocodes each address using the local BAN database,
    and returns a DataFrame with the original addresses and their corresponding latitude and longitude.

    Parameters:
    - input_file (str): The file path of the text file containing addresses to geocode. Each address
                        should be on a separate line.
    - database (str): The file path of the SQLite database containing the BAN data.
    - processes (int): The number of worker processes to use for multiprocessing.
    - verbose (bool): If set to True, additional information will be printed to the console during execution.

    Returns:
    - geocoded (DataFrame): A pandas DataFrame with columns 'Address', 'Latitude', and 'Longitude'.
                            Each row contains the original address and its geocoded coordinates.
    """
    # Initialize the AddressesMatcher class with the provided database, number of processes, and verbosity
    matcher = AddressesMatcher(database=database, num_processes=processes, verbose=verbose)

    # Use the geocode_addresses method to geocode the addresses from the input file
    addresses_geocoded = matcher.geocode_addresses(input_file=input_file)

    # Prepare lists to store individual latitude and longitude values
    latitudes = []
    longitudes = []

    # Obtain the list of addresses from the geocoded results
    addresses = list(addresses_geocoded.keys())

    # Iterate through the geocoded coordinates and split them into latitude and longitude
    for coords in addresses_geocoded.values():
        lat, lon = coords.split(', ')
        latitudes.append(lat)
        longitudes.append(lon)

    # Create a DataFrame with the addresses and their corresponding latitude and longitude
    geocoded = pd.DataFrame({
        'Address': addresses,
        'Latitude': latitudes,
        'Longitude': longitudes
    })

    # Return the DataFrame containing the geocoded data
    return geocoded
