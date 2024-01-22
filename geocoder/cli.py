import click
import pandas as pd
from .geocoder import perform_geocoding
from .exporter import export_to_csv, export_to_sqlite
from .database import import_csv_to_sqlite
from .utils import uncompress_gz_to_csv, download_csv

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
        print(geocoded[["geometry_coordinates", "properties_label"]].to_string(index=False))
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
        if not verbose and not sqlite and not output_csv:
            print(geocoded[["geometry_coordinates", "properties_label"]].to_string(index=False))
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
        print(geocoded[["geometry_coordinates", "properties_label"]].to_string(index=False))
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
    if not verbose and not sqlite and not output_csv:
        print(geocoded[["geometry_coordinates", "properties_label"]].to_string(index=False))
    return geocoded


@click.command(name="initdb")
@click.option('--ban-url', '-csv', type=str, help='URL or file path to the BAN (Base Adresse Nationale) CSV datasheet.',
              default='https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/adresses-france.csv.gz', show_default=True)
@click.option('--ban-db', '-db', type=click.Path(writable=True), default='ban.db', show_default=True,
              help='File path to the SQLite database.')
@click.option('--separator', '-sep', default=";", show_default=True, help='CSV field separator.')
@click.option('--chunksize', '-chk', default=10000, show_default=True, help='Number of rows per chunk to process.')
@click.option('--verbose', '-v', is_flag=True, help="More information displayed.")
def initdb(ban_url, ban_db, separator, chunksize, verbose):
    """
    Creating local database with BAN datasheet to geocoding offline.
    """
    ban_gz = ban_url.split("/")[-1]
    ban_csv = ban_gz.replace(".csv.gz", ".csv")

    # Download the CSV.GZ file from the provided URL
    download_csv(url=ban_url, output_path=ban_gz, verbose=verbose)  # This function should return the path to the downloaded file

    # Uncompress the GZ file to CSV
    uncompress_gz_to_csv(gz_file_path=ban_gz, csv_file_path=ban_csv, verbose=verbose)  # This function should return the path to the uncompressed CSV

    # Import the CSV into the SQLite database
    import_csv_to_sqlite(csv_file_path=ban_csv, sqlite_db_path=ban_db, table_name="adresses-france",
                         separator=separator, chunksize=chunksize, verbose=verbose)


cli.add_command(geocoding)
cli.add_command(geocoding_from_file)
cli.add_command(initdb)
