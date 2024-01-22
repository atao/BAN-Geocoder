import pandas as pd
import sqlite3

def export_to_csv(data, file, mode, header, index, verbose):
    """
    Export data to a CSV file.

    Parameters:
    - data (DataFrame): The pandas DataFrame to export.
    - file (str): The file path where the CSV will be saved.
    - mode (str): Writing mode for the CSV file ('w' for write, 'a' for append, etc.).
    - header (bool): Flag to include the header row in the CSV output.
    - index (bool): Flag to include the DataFrame index in the CSV output.
    - verbose (bool): Flag to enable verbose output, which prints additional information.
    """
    if not file.endswith(".csv"):
        file = "{}.csv".format(file)
    if verbose:
        print('[+] Data exported successfully to "{}".'.format(file))
    data.to_csv(file, index=index, mode=mode, header=header)


def export_to_sqlite(data, database, table, mode, index, verbose):
    """
    Export data to an SQLite database.

    Parameters:
    - data (DataFrame): The pandas DataFrame to export.
    - database (str): The file path of the SQLite database.
    - table (str): The name of the table to insert data into in the SQLite database.
    - mode (str): How to behave if the table already exists ('fail', 'replace', 'append').
    - index (bool): Flag to include the DataFrame index in the SQLite output.
    - verbose (bool): Flag to enable verbose output, which prints additional information.
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