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

    @staticmethod
    def standardize_address(address):
        """
        Replace common abbreviations in the address string.
        """
        replacements = {
            # Norme XP Z 10-011
            "ALL": "ALLÉE",
            "AV": "AVENUE",
            "BD": "BOULEVARD",
            "CTRE": "CENTRE",
            "CCAL": "CENTRE COMMERCIAL",
            "CHEM": "CHEMIN",
            "IMM": "IMMEUBLE",
            "IMM": "IMMEUBLES",
            "IMP": "IMPASSE",
            "LD": "LIEU-DIT",
            "LOT": "LOTISSEMENT",
            "PAS": "PASSAGE",
            "PL": "PLACE",
            "RES": "RÉSIDENCE",
            "RPT": "ROND-POINT",
            "RTE": "ROUTE",
            "SENT": "SENTIER",
            "SQ": "SQUARE",
            "VLGE": "VILLAGE",
            "ZA": "ZONE D’ACTIVITÉ",
            "ZAC": "ZONE D’AMÉNAGEMENT CONCERTÉ",
            "ZAD": "ZONE D’AMÉNAGEMENT DIFFÉRÉ",
            "ZI": "ZONE INDUSTRIELLE",

            # Norme XP Z 10-011
            "ADJ": "ADJUDANT",
            "AERD": "AÉRODROME",
            "AERG": "AÉROGARE",
            "AERN": "AÉORONAUTIQUE",
            "AERP": "AÉROPORT",
            "AGCE": "AGENCE",
            "AGRIC": "AGRICOLE",
            "ANC": "ANCIEN",
            "ANC": "ANCIENNEMENT",
            "APP": "APPARTEMENT",
            "APP": "APPARTEMENTS",
            "ARMT": "ARMEMENT",
            "ARR": "ARRONDISSEMENT",
            "ASP": "ASPIRANT",
            "ASSOC": "ASSOCIATION",
            "ASSUR": "ASSURANCE",
            "AT": "ATELIER",
            "BRQ": "BARAQUEMENT",
            "BAS": "BAS",
            "BAS": "BASSE",
            "BAS": "BASSES",
            "BTN": "BATAILLON",
            "BTN": "BATAILLONS",
            "BAT": "BÂTIMENT",
            "BAT": "BÂTIMENTS",
            "B": "BIS",
            "BP": "BOITE POSTALE",
            "CAB": "CABINET",
            "CANT": "CANTON",
            "CDL": "CARDINAL",
            "CP": "CASE POSTALE",
            "CHBR": "CHAMBRE",
            "CTD": "CITADELLE",
            "COLL": "COLLÈGE",
            "CNL": "COLONEL",
            "COLO": "COLONIE",
            "CTE": "COMITÉ",
            "CDT": "COMMANDANT",
            "CIAL": "COMMERCIAL",
            "COM": "COMMUNE",
            "COM": "COMMUNEAL",
            "COM": "COMMUNEAUX",
            "CIE": "COMPAGNIE",
            "COMP": "COMPAGNON",
            "COMP": "COMPAGNONS",
            "COOP": "COOPÉRATIVE",
            "CS": "COURSE SPÉCIALE",
            "CRX": "CROIX",
            "DELEG": "DÉLÉGATION",
            "DEP": "DÉPARTEMENTAL",
            "DEP": "DÉPARTEMENTALAUX",
            "DIR": "DIRECTEUR",
            "DIR": "DIRECTEURCTION",
            "DIV": "DIVISION",
            "DR": "DOCTEUR",
            "ECO": "ECONOMIE",
            "ECO": "ECONOMIEQUE",
            "ECRIV": "ECRIVAIN",
            "ENST": "ENSEIGNEMENT",
            "ENS": "ENSEMBLE",
            "ENT": "ENTRÉE",
            "ENT": "ENTRÉES",
            "ENTR": "ENTREPRISE",
            "EP": "EPOUX",
            "EP": "EPOUSE",
            "ETS": "ETABLISSEMENT",
            "ETG": "ETAGE",
            "EM": "ETAT MAJOR",
            "EVQ": "EVÊQUE",
            "FAC": "FACULTÉ",
            "FOR": "FORÊT",
            "FOR": "FORESTIER",
            "FR": "FRANÇAIS",
            "FR": "FRANÇAISE",
            "FUS": "FUSILIER",
            "GEND": "GENDARMERIE",
            "GAL": "GÉNÉRAL",
            "GOUV": "GOUVERNEMENTAL",
            "GOU": "GOUVERNEUR",
            "GD": "GRAND",
            "GDE": "GRANDE",
            "GDES": "GRANDES",
            "GDS": "GRANDS",
            "HT": "HAUT",
            "HTE": "HAUTE",
            "HTES": "HAUTES",
            "HTS": "HAUTS",
            "HOP": "HÔPITAL",
            "HOP": "HÔPITAUX",
            "HOSP": "HOSPICE",
            "HOSP": "HOSPITALIER",
            "HOT": "HÔTEL",
            "INFANT": "INFANTERIE",
            "INF": "INFÉRIEUR",
            "INF": "INFÉRIEURE",
            "ING": "INGÉNIEUR",
            "INSP": "INSPECTEUR",
            "INST": "INSTITUT",
            "INTERN": "INTERNATIONAL",
            "INTERN": "INTERNATIONALE",
            "LABO": "LABORATOIRE",
            "LT": "LIEUTENANT",
            "LTDV": "LIEUTENANT DE VAISSEAU",
            "MME": "MADAME",
            "MLLE": "MADEMOISELLE",
            "MAG": "MAGASIN",
            "MAIS": "MAISON",
            "ME": "MAÎTRE",
            "MAL": "MARÉCHAL",
            "MAR": "MARITIME",
            "MED": "MÉDECIN",
            "MED": "MÉDICAL",
            "MMES": "MESDAMES",
            "MLLES": "MESDEMOISELLES",
            "MM": "MESSIEURS",
            "MIL": "MILITAIRE",
            "MIN": "MINISTÈRE",
            "MGR": "MONSEIGNEUR",
            "M": "MONSIEUR",
            "MUN": "MUNICIPAL",
            "MUT": "MUTUEL",
            "NAL": "NATIONAL",
            "ND": "NOTRE DAME",
            "NOUV": "NOUVEAU",
            "NOUV": "NOUVELLE",
            "OBS": "OBSERVATOIRE",
            "PAST": "PASTEUR",
            "PT": "PETIT",
            "PTE": "PETITE",
            "PTES": "PETITES",
            "PTS": "PETITS",
            "POL": "POLICE",
            "PREF": "PRÉFET",
            "PREF": "PRÉFÉCTURE",
            "PDT": "PRÉSIDENT",
            "PR": "PROFESSEUR",
            "PROF": "PROFESSIONEL",
            "PROF": "PROFESSIONELE",
            "PROL": "PROLONGÉ",
            "PROL": "PROLONGÉE",
            "PROP": "PROPRIÉTÉ",
            "Q": "QUATER",
            "C": "QUINQUIES",
            "RECT": "RECTEUR",
            "RGT": "RÉGIMENT",
            "REG": "RÉGION",
            "REG": "RÉGIONAL",
            "REP": "RÉPUBLIQUE",
            "REST": "RESTAURANT",
            "ST": "SAINT",
            "STE": "SAINTE",
            "STES": "SAINTES",
            "STS": "SAINTS",
            "SANA": "SANATORIUM",
            "SGT": "SERGENT",
            "SCE": "SERVICE",
            "SOC": "SOCIÉTÉ",
            "SC": "SOUS COUVERT",
            "SPREF": "SOUS-PRÉFET",
            "SUP": "SUPÉRIEUR",
            "SUP": "SUPÉRIEURE",
            "SYND": "SYNDICAT",
            "TECH": "TECHNICIEN",
            "TECH": "TECHNIQUE",
            "T": "TER",
            "TSA": "TRI SERVICE ARRIVÉE",
            "TUN": "TUNNEL",
            "UNVT": "UNIVERSITAIRE",
            "UNIV": "UNIVERSITÉ",
            "VELOD": "VÉLODROME",
            "VVE": "VEUVE",
            "VIEL": "VIEILLE",
            "VIEL": "VIEILLES",
            "VX": "VIEUX",

            # Added
            "R": "RUE",
        }

        # Remove ","
        address = address.replace(",", "").strip()
        address = address.replace(";", "").strip()
        address = address.replace(":", "").strip()

        parts = address.split()
        if len(parts) > 1:
            n = 0
            while n != len(parts):
                if parts[n].upper() in replacements:
                    for val in replacements:
                        if parts[n].upper() == val:
                            parts[n] = replacements[val].capitalize()
                n = n + 1
            standardized_address = ' '.join(parts)
        else:
            standardized_address = address
        return standardized_address

    def geocode_addresses(self, input_file):
        """
        Geocode a list of addresses using multiple processes.
        """
        if self.verbose:
            print("[+] Geocoding addresses...")

        # Initialize the pool of worker processes once
        pool = Pool(processes=self.num_processes)

        # Create a dictionary to store the best match for each input address
        best_matches = {}
        geocoded = {}

        # Open database for requests
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        keywords = ['Allée', 'Avenue', 'Boulevard', 'Centre', 'Centre commercial', 'Chemin', 'Immeuble',
                    'Immeubles', 'Impasse', 'Lieu-dit', 'Lieu dit', 'Lotissement', 'Passage', 'Place', 'Résidence',
                    'Rond-point', 'Route', 'Sentier', 'Square', 'Village', 'Zone d’activité',
                    'Zone d’aménagement concerté', 'Zone d’aménagement différé', 'Zone industrielle']

        with open(input_file, "r") as addresses_to_geocode:

            # Process each address to geocode
            for address_to_geocode in addresses_to_geocode:
                address_to_geocode = address_to_geocode.strip()
                if len(address_to_geocode) != 0:
                    # Standardize the address before processing
                    standardized_address = self.standardize_address(address_to_geocode)

                    # Extract the starting number from the input address using regular expression
                    starting_number_match = re.match(r'^\d+', standardized_address)
                    starting_number = starting_number_match.group(0) if starting_number_match else None

                    # Attempt to extract a 5-digit postal code from the input address
                    postal_code_match = re.search(r'\b\d{5}\b', standardized_address)
                    postal_code = postal_code_match.group(0) if postal_code_match else None

                    # Determine if the first or second word is one of the keywords
                    address_parts = standardized_address.split(maxsplit=2)  # Split into parts
                    potential_keywords = [address_parts[0]]  # Assume first part is a keyword
                    if starting_number and len(address_parts) > 1:
                        # If the first part is a number, consider the second part as a keyword
                        potential_keywords = [address_parts[1]]

                    # Create a nom_afnor WHERE clause to match any entry starting with the keyword
                    nom_afnor_clause = '1=1'  # Default to true if no keyword is matched
                    for keyword in keywords:
                        if keyword.upper() in standardized_address.upper():
                            # Use the UPPER function to perform case-insensitive match
                            nom_afnor_clause = f"nom_afnor LIKE '%{keyword.upper()}%"
                            pattern_word = re.compile(r'\b(\w+)\b \d+')
                            m = re.search(pattern_word, standardized_address)
                            if m is not None:
                                nom_afnor_clause = f"{nom_afnor_clause}{m.group(1).upper()}%'"
                            else:
                                nom_afnor_clause = f"{nom_afnor_clause}'"
                            break  # Stop after the first match

                    # If a starting number is found, include it in the SQL WHERE clause
                    number_clause = f"numero = {starting_number}" if starting_number else "1=1"

                    # If a postal code is found, include it in the SQL WHERE clause
                    postal_code_clause = f"code_postal = {postal_code}" if postal_code else "1=1"

                    # Combine the two clauses with an AND operator
                    where_clause = f"{number_clause} AND {postal_code_clause} AND {nom_afnor_clause}"

                    # Address query with consideration for "rep" values and the "where_clause"
                    sqlquery = f"""SELECT CASE WHEN rep IS NOT NULL AND trim(rep) != '' THEN numero || ' ' || rep || ' ' 
                    || nom_voie ELSE numero || ' ' || nom_voie END || ' ' || code_postal || ' ' || nom_commune AS address, 
                    lat, lon FROM addresses WHERE {where_clause}"""
                    cursor.execute(sqlquery)

                    # Fetch the results including address, lat, and lon
                    address_results = cursor.fetchall()
                    addresses = [row[0] for row in address_results]
                    address_lat_lon_map = {row[0]: (row[1], row[2]) for row in address_results}

                    # Split the address list into chunks for each process
                    chunks = [addresses[i::self.num_processes] for i in range(self.num_processes)]
                    results = pool.map(self.match_address, [(standardized_address, chunk) for chunk in chunks])
                    # Filter out None results
                    results = [result for result in results if result is not None]

                    # Find the best overall match from the results
                    best_match = max(results, key=lambda x: x[1]) if results else None
                    best_matches[standardized_address] = best_match

                    # After finding the best match, get the lat and lon from the dictionary
                    if best_match:
                        matched_address, match_score = best_match
                        lat, lon = address_lat_lon_map.get(matched_address, (None, None))
                        if lat is not None and lon is not None:
                            geocoded[matched_address] = "{}, {}".format(lat, lon)
                            if self.verbose:
                                print(
                                    f'[+] Best match for "{standardized_address}"\t--->\t{matched_address} [{lat}, {lon}] with a score of {match_score}')
                        else:
                            if self.verbose:
                                print(f'Coordinates for matched address "{matched_address}" not found.')
                            pass
                    else:
                        if self.verbose:
                            print(f'No match found for "{standardized_address}".')
                        pass
                else:
                    pass

            # Close the pool of worker processes after processing all addresses
            pool.close()
            pool.join()

            # Now it's safe to close the database connection
            conn.close()
            return geocoded
