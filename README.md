# BAN-Geocoder
Geocoding addresses using the national address database API - https://adresse.data.gouv.fr/ - BAN

```shell
root@kali:~# python3 ban_geocoder.py -h
usage: ban_geocoder.py [-h] [-v] [-a ADDRESS] [--lat LAT] [--lon LON] [-s]
                       [-g] [--csv] [--version]

Geocoding addresses using the national address database API -
https://adresse.data.gouv.fr/ - BAN The data come from IGN, La Poste, DGFiP,
Etalab and OpenStreetMap France.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -a ADDRESS, --address ADDRESS
                        enter the address to geocoder
  -s, --score           show score
  -g, --gps             show coordinates
  --csv                 show all in csv format
  --version             show version

  --lat LAT, --latitude LAT
                        enter Latitude
  --lon LON, --longitude LON
                        enter Longitude
```
