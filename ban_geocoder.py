#!/usr/bin/python
# -*- coding: utf-8 -*

import json
import sqlite3
import sys
import urllib.parse

import click
import pandas as pd
import requests


@click.group
def cli():
    pass


@click.command(name="geo")
@click.option('--address', '-a', help='Address to geocode', type=str, required=True)
@click.option('--limit', '-l', default=0, help='Number of results for each geocoding.', show_default=True, type=int)
@click.option('--output-csv', '-csv', type=click.Path(writable=True),
              help='Path to CSV file where results will be saved.')
@click.option('--include-header', '-hdr', is_flag=True, default=False, show_default=True,
              help='Include header row in the CSV output.')
@click.option('--include-index', '-idx', is_flag=True, default=False, show_default=True,
              help='Include DataFrame index in the CSV / SQL output.')
@click.option('--sqlite', '-d', type=click.Path(writable=True),
              help='Path to SQLite database file where results will be saved.')
@click.option('--table-name', '-t', type=str, default="data", show_default=True,
              help='Name of the table to insert data into in the SQLite database.')
@click.option('--mode', '-m', type=click.Choice(['fail', 'replace', 'append'], case_sensitive=False), default="append",
              show_default=True, help='How to behave if the file already exists.')
@click.option('--verbose', '-v', is_flag=True, help="More information displayed.")
def geocoding(address, limit, output_csv, sqlite, table_name, include_header, mode, include_index, verbose):
    """
        Geocoding a single address.
    """
    geocoded = perform_geocoding(address, limit, verbose)
    if verbose:
        print("-------------------------------------------------------------")
        print(geocoded[["geometry_coordinates", "properties_label"]])
        print("-------------------------------------------------------------")
    if geocoded is not None:
        if output_csv is not None:
            if mode == "fail":
                csvmode = "x"
            elif mode == "replace":
                csvmode = "w"
            else:
                csvmode = "a"
            export_to_csv(geocoded, file=output_csv, mode=csvmode, header=include_header, index=include_index,
                          verbose=verbose)
        if sqlite is not None:
            export_to_sqlite(geocoded, database=sqlite, table=table_name, mode=mode, index=include_index,
                             verbose=verbose)
    else:
        click.echo(f'No results found for {address}')


@click.command(name="file")
@click.option('--input-file', '-i', help='Addresses file to geocode', required=True, type=click.Path(exists=True))
@click.option('--limit', '-l', default=0, help='Number of results for each geocoding.', show_default=True, type=int)
@click.option('--output-csv', '-csv', type=click.Path(writable=True),
              help='Path to CSV file where results will be saved.')
@click.option('--include-header', '-hdr', is_flag=True, default=False, show_default=True,
              help='Include header row in the CSV output.')
@click.option('--include-index', '-idx', is_flag=True, default=False, show_default=True,
              help='Include DataFrame index in the CSV / SQL output.')
@click.option('--sqlite', '-d', type=click.Path(writable=True),
              help='Path to SQLite database file where results will be saved.')
@click.option('--table-name', '-t', type=str, default="data", show_default=True,
              help='Name of the table to insert data into in the SQLite database.')
@click.option('--mode', '-m', type=click.Choice(['fail', 'replace', 'append'], case_sensitive=False), default="append",
              show_default=True, help='How to behave if the file already exists.')
@click.option('--verbose', '-v', is_flag=True, help="More information displayed.")
def geocoding_from_file(input_file, limit, output_csv, sqlite, table_name, include_header, mode, include_index,
                        verbose):
    """
    Geocoding addresses from file.
    """
    if verbose:
        print("[+] Reading file {}".format(input_file))
    with open(input_file, "r") as f:
        geocoded = pd.DataFrame()
        for line in f:
            geocoded = geocoded._append(perform_geocoding(line, limit, verbose))
    if verbose:
        print("-------------------------------------------------------------")
        print(geocoded[["geometry_coordinates", "properties_label"]])
        print("-------------------------------------------------------------")
    if output_csv is not None:
        if mode == "fail":
            csvmode = "x"
        elif mode == "replace":
            csvmode = "w"
        else:
            csvmode = "a"
        export_to_csv(geocoded, file=output_csv, mode=csvmode, header=include_header, index=include_index,
                      verbose=verbose)
    if sqlite is not None:
        export_to_sqlite(geocoded, database=sqlite, table=table_name, mode=mode, index=include_index, verbose=verbose)
    return geocoded


def perform_geocoding(address, limit, verbose):
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
        geocoded = df.loc[:limit].copy()
        return geocoded
    else:
        return None


def export_to_csv(data, file, mode, header, index, verbose):
    """
    Export data to a CSV file.
    """
    if not file.endswith(".csv"):
        file = "{}.csv".format(file)
    if verbose:
        print('[+] Data exported successfully to "{}".'.format(file))
    data.to_csv(file, index=index, mode=mode, header=header)


def export_to_sqlite(data, database, table, mode, index, verbose):
    """
    Export data to an SQLite database.
    """
    if not database.endswith(".db"):
        database = '{}.db'.format(database)
    if verbose:
        print('[+] Data exported successfully to table "{}" in database "{}".'.format(table, database))
    conn = sqlite3.connect(database)
    try:
        # Convert any list in the DataFrame to a string representation
        for column in data.columns:
            if data[column].apply(lambda x: isinstance(x, list)).any():
                # Here we join the list items into a string separated by a comma
                data[column] = data[column].apply(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)

        data.to_sql(con=conn, name=table, if_exists=mode, index=index)
    except ValueError as e:
        print("[!] Error : {}".format(e))
        exit(1)
    finally:
        conn.close()


cli.add_command(geocoding)
cli.add_command(geocoding_from_file)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        cli.main(['--help'])
    else:
        cli()
