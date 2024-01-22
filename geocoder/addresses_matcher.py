import re
import sqlite3
from multiprocessing import Pool

from thefuzz import process


class AddressesMatcher:
    def __init__(self, database, num_processes, verbose=False):
        self.database = database
        self.verbose = verbose
        self.num_processes = num_processes

    @staticmethod
    def match_address(args):
        """
        Match an address using thefuzz library to find the best match from a list of addresses.
        """
        input_address, addresses = args
        return process.extractOne(input_address, addresses)

    def geocode_addresses(self, input_file):
        """
        Geocode a list of addresses using multiple processes.
        """
        if self.verbose:
            print("[+] Geocoding addresses...")

        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        # Fetch all addresses from the database and store them in memory
        if self.verbose:
            print(f"[+] Fetching addresses from {self.database}...")
        cursor.execute(
            "SELECT numero || ' ' || rep || ' ' || nom_voie || ' ' || code_postal || ' ' || nom_commune AS address FROM addresses")
        addresses = [row[0] for row in cursor.fetchall()]
        conn.close()  # Close the connection after fetching the data

        # Initialize the pool of worker processes once
        pool = Pool(processes=self.num_processes)

        # Create a dictionary to store the best match for each input address
        best_matches = {}
        geocoded = {}

        # Open database for requests
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        with open(input_file, "r") as addresses_to_geocode:

            # Process each address to geocode
            for address_to_geocode in addresses_to_geocode:
                address_to_geocode = address_to_geocode.strip()

                # Extract the starting number from the input address using regular expression
                starting_number_match = re.match(r'^\d+', address_to_geocode)
                starting_number = starting_number_match.group(0) if starting_number_match else None

                # Attempt to extract a 5-digit postal code from the input address
                postal_code_match = re.search(r'\b\d{5}\b', address_to_geocode)
                postal_code = postal_code_match.group(0) if postal_code_match else None

                # If a starting number is found, include it in the SQL WHERE clause
                number_clause = f"numero = {starting_number}" if starting_number else "1=1"

                # If a postal code is found, include it in the SQL WHERE clause
                postal_code_clause = f"code_postal = {postal_code}" if postal_code else "1=1"

                # Combine the two clauses with an AND operator
                where_clause = f"{number_clause} AND {postal_code_clause}"

                # Address query with consideration for "rep" values and the "where_clause"
                cursor.execute(f""" SELECT CASE WHEN rep IS NOT NULL AND trim(rep) != '' THEN numero || ' ' || rep || ' ' 
                || nom_voie ELSE numero || ' ' || nom_voie END || ' ' || code_postal || ' ' || nom_commune AS address, 
                lat, lon FROM addresses WHERE {where_clause}
                            """)

                # Fetch the results including address, lat, and lon
                address_results = cursor.fetchall()
                addresses = [row[0] for row in address_results]
                address_lat_lon_map = {row[0]: (row[1], row[2]) for row in address_results}

                # Split the address list into chunks for each process
                chunks = [addresses[i::self.num_processes] for i in range(self.num_processes)]
                results = pool.map(self.match_address, [(address_to_geocode, chunk) for chunk in chunks])
                # Filter out None results
                results = [result for result in results if result is not None]

                # Find the best overall match from the results
                best_match = max(results, key=lambda x: x[1]) if results else None
                best_matches[address_to_geocode] = best_match

                # After finding the best match, get the lat and lon from the dictionary
                if best_match:
                    matched_address, match_score = best_match
                    lat, lon = address_lat_lon_map.get(matched_address, (None, None))
                    if lat is not None and lon is not None:
                        geocoded[matched_address] = "{}, {}".format(lat, lon)
                        if self.verbose:
                            print(f'[+] Best match for "{address_to_geocode}"\t--->\t{matched_address} [{lat}, {lon}] with a score of {match_score}')
                    else:
                        if self.verbose:
                            print(f'Coordinates for matched address "{matched_address}" not found.')
                        pass
                else:
                    if self.verbose:
                        print(f'No match found for "{address_to_geocode}".')
                    pass

            # Close the pool of worker processes after processing all addresses
            pool.close()
            pool.join()

            # Now it's safe to close the database connection
            conn.close()
            return geocoded
