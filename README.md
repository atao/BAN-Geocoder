[![Pylint](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml/badge.svg)](https://github.com/atao/BAN-Geocoder/actions/workflows/pylint.yml)
# Geocoder for adresse.data.gouv.fr
Geocoding addresses using the national address database API - [adresse.data.gouv.fr](https://adresse.data.gouv.fr/).

## Requirements
```
pip install -r requirements.txt
```

## Usage and options
```
Usage: ban_geocoder.py [OPTIONS]

Options:
  -v, --verbose       Verbose mode
  -a, --address TEXT  Address to be geocoded  [required]
  -n, --nb INTEGER    Number of results to return  [default=1]
  -h, --help          Show this message and exit.
```

## Example
```
Me # python ban_geocoder.py -a "55 rue Faubourg Saint-Honoré" -v
Geocoding addresses using the national address database API - https://adresse.data.gouv.fr/ - BAN
[+] Geocoding address...
Longitude  Latitude   Score              Address
48.87063   2.316931   0.8035072727272727 55 Rue du Faubourg Saint-Honoré 75008 Paris
```

## See also
* [BanR](https://github.com/joelgombin/banR) : R client for the BAN API
* [tidygeocoder](https://github.com/jessecambon/tidygeocoder), r package similar to banR using other geocoding services such as US Census geocoder, Nominatim (OSM), Geocodio, and Location IQ.
