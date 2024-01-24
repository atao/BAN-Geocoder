[![Pylint](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml/badge.svg)](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml)
# BAN Geocoder
🗺️ Geocoding addresses with BAN !

## Features
- Geocoding online using the [Base Adresse Nationale API](https://adresse.data.gouv.fr/)
- Geocoding offline using a local BAN database created with [CSV from BAN](https://adresse.data.gouv.fr/data/ban/adresses/latest/csv).

## Purpose
The [Base Adresse Nationale (BAN)](https://adresse.data.gouv.fr/) is the reference address database in France, containing the correspondence between non-nominative addresses (number, street name, lieu-dit and commune) and the geographical position of over 25 million addresses in France.

## Requirements
```
pip install -r requirements.txt
```

## Usage and options
```
Usage: ban_geocoder.py [OPTIONS] COMMAND [ARGS]...

  🗺️ Geocoding addresses with BAN !

Options:
  --help  Show this message and exit.

Commands:
  file    Geocoding addresses from file.
  geo     Geocoding a single address.
  initdb  Creating local database with BAN datasheet to geocoding offline.
  local   Local geocoding using BAN database.
```
- *Command file*
```
Usage: ban_geocoder.py file [OPTIONS]

  Geocoding addresses from file.

Options:
  -i, --input-file PATH           Addresses file to geocode  [required]
  -l, --limit INTEGER             Number of results for each geocoding.
                                  [default: 0]
  -csv, --output-csv PATH         Path to CSV file where results will be
                                  saved.
  -hdr, --include-header          Include header row in the CSV output.
  -idx, --include-index           Include DataFrame index in the CSV / SQL
                                  output.
  -db, --output-db PATH           Path to SQLite database file where results
                                  will be saved.
  -t, --table-name TEXT           Name of the table to insert data into in the
                                  SQLite database.  [default: data]
  -m, --mode [fail|replace|append]
                                  How to behave if the file already exists.
                                  [default: append]
  -v, --verbose                   More information displayed.
  --help                          Show this message and exit.
```
- *Command geo*
```
Usage: ban_geocoder.py geo [OPTIONS]

  Geocoding a single address.

Options:
  -a, --address TEXT              Address to geocode  [required]
  -l, --limit INTEGER             Number of results for each geocoding.
                                  [default: 0]
  -csv, --output-csv PATH         Path to CSV file where results will be
                                  saved.
  -hdr, --include-header          Include header row in the CSV output.
  -idx, --include-index           Include DataFrame index in the CSV / SQL
                                  output.
  -db, --output-db PATH           Path to SQLite database file where results
                                  will be saved.
  -t, --table-name TEXT           Name of the table to insert data into in the
                                  SQLite database.  [default: data]
  -m, --mode [fail|replace|append]
                                  How to behave if the file already exists.
                                  [default: append]
  -v, --verbose                   More information displayed.
  --help                          Show this message and exit.
```
- *Command initdb*
```
Options:                                                                    
  -csv, --ban-datasheet TEXT  Department number related of BAN (Base Adresse
                              Nationale) CSV datasheet.  [default: france]
  -db, --ban-db PATH          File path to the SQLite database.  [default:
                              ban.db]
  -sep, --separator TEXT      CSV field separator.  [default: ;]
  -chk, --chunksize INTEGER   Number of rows per chunk to process.  [default:
                              10000]
  -v, --verbose               More information displayed.
  --help                      Show this message and exit.
```
- *Command local*
```
Usage: ban_geocoder.py local [OPTIONS]

  Local geocoding using BAN database.

Options:
  -i, --input-file PATH           Addresses file to geocode  [required]
  -ban, --local-database TEXT     Local BAN database for geocoding.
                                  [required]
  -p, --processes INTEGER         Adjust the number of processes based on your
                                  machine for calculations.  [default: 12]
  -csv, --output-csv PATH         Path to CSV file where results will be
                                  saved.
  -hdr, --include-header          Include header row in the CSV output.
  -idx, --include-index           Include DataFrame index in the CSV / SQL
                                  output.
  -db, --output-db PATH           Path to SQLite database file where results
                                  will be saved.
  -t, --table-name TEXT           Name of the table to insert data into in the
                                  SQLite database.  [default: data]
  -m, --mode [fail|replace|append]
                                  How to behave if the file already exists.
                                  [default: append]
  -v, --verbose                   More information displayed.
  --help                          Show this message and exit.

```

## Examples
*with csv export*
```
(.venv) ME > python .\ban_geocoder.py geo -a "55 rue Faubourg Saint-Honoré" -v -csv address
[+] Geocoding address : 55 rue Faubourg Saint-Honoré
-------------------------------------------------------------
   geometry_coordinates                             properties_label
   [48.87063, 2.316931]  55 Rue du Faubourg Saint-Honoré 75008 Paris
-------------------------------------------------------------
[+] Data exported successfully to "address.csv".
```
*with database export*
```
(.venv) ME > python .\ban_geocoder.py geo -a "55 rue Faubourg Saint-Honoré" -v -d address
[+] Geocoding address : 55 rue Faubourg Saint-Honoré
-------------------------------------------------------------
   geometry_coordinates                             properties_label
   [48.87063, 2.316931]  55 Rue du Faubourg Saint-Honoré 75008 Paris
-------------------------------------------------------------
[+] Data exported successfully to table "data" in database "address.db".
```
*create a local BAN database with addresses from department 31*
```
(.venv) ME > python .\ban_geocoder.py initdb --ban-datasheet 31 --ban-db ban.db -v
[+] Downloading BAN datasheet from https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/adresses-31.csv.gz
[+] File downloaded successfully: adresses-31.csv.gz
[+] Uncompressing adresses-31.csv.gz to adresses-31.csv
[+] Importing adresses-31.csv into SQLite database ban.db...
[+] Database ban.db with table addresses_france created succesfully !
[+] Optimize database...
[+] Indexes in ban.db was created succesfully !
```
*using using local BAN database*
```
(.venv) ME > python .\ban_geocoder.py local -i .\data.txt --local-database .\ban.db -p 20 -v
[+] Geocoding addresses...
[+] Fetching addresses from .\ban.db...
[+] Best match for "16 boulevard THIERS     21000   DIJON"  --->    16 Boulevard Thiers 21000 Dijon [47.323686, 5.049228] with a score of 100
[+] Best match for "1 rue DE VELARS 21320   POUILLY EN AUXOIS"      --->    1 Rue de Velard 21320 Pouilly-en-Auxois [47.265765, 4.554323] with a score of 97
[+] Best match for "Rue Claude Petiet       21400   CHATILLON SUR SEINE"    --->    2 Rue Claude Petiet 21400 Châtillon-sur-Seine [47.861858, 4.559604] with a score of 97
[+] Best match for "21 rue de la Mare       21380   SAVIGNY LE SEC" --->    21 Rue de la Mare 21380 Savigny-le-Sec [47.431938, 5.050335] with a score of 100
```


## See also
* [BanR](https://github.com/joelgombin/banR) : R client for the BAN API
* [tidygeocoder](https://github.com/jessecambon/tidygeocoder), r package similar to banR using other geocoding services such as US Census geocoder, Nominatim (OSM), Geocodio, and Location IQ.
