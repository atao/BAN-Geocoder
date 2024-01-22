[![Pylint](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml/badge.svg)](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml)
# BAN Geocoder
🗺️ Geocoding addresses with BAN !

## Purpose
The [Base Adresse Nationale (BAN)](https://adresse.data.gouv.fr/) is the reference address database in France, containing the correspondence between non-nominative addresses (number, street name, lieu-dit and commune) and the geographical position of over 25 million addresses in France.

## Requirements
```
pip install -r requirements.txt
```

## Usage and options
```
Usage: ban_geocoder.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  file  Geocoding addresses from file.
  geo   Geocoding a single address.

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
  -d, --sqlite PATH               Path to SQLite database file where results
                                  will be saved.
  -t, --table-name TEXT           Name of the table to insert data into in the
                                  SQLite database.  [default: data]
  -m, --mode [fail|replace|append]
                                  How to behave if the file already exists.
                                  [default: append]
  -v, --verbose                   More information displayed.
  --help                          Show this message and exit.
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
  -d, --sqlite PATH               Path to SQLite database file where results
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

## See also
* [BanR](https://github.com/joelgombin/banR) : R client for the BAN API
* [tidygeocoder](https://github.com/jessecambon/tidygeocoder), r package similar to banR using other geocoding services such as US Census geocoder, Nominatim (OSM), Geocodio, and Location IQ.
