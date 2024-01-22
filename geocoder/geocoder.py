import json
import urllib.parse

import pandas as pd
import requests


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
