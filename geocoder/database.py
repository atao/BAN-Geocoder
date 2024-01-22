import pandas as pd
import sqlite3


def import_csv_to_sqlite(csv_file_path, sqlite_db_path, table_name, separator, verbose, chunksize=10000):
    """
    Import a large CSV file into a SQLite database in chunks.

    Parameters:
    - csv_file_path (str): The file path of the CSV file to import.
    - sqlite_db_path (str): The file path of the SQLite database.
    - table_name (str): The name of the table to insert the data into.
    - separator (str): The delimiter to use for separating entries in the CSV file.
    - chunksize (int): The number of rows per chunk to process at a time. A larger chunksize can
                       be faster for writing data, but it may also consume more memory.

    Notes:
    - This function assumes that the SQLite database and table already exist.
    - The function appends each chunk of data to the specified table. If the table does not exist,
      pandas will create it based on the DataFrame's schema.
    - It is recommended to ensure that the table schema in SQLite matches the CSV file structure.
    - In case of large CSV files, the 'chunksize' parameter can be adjusted to avoid memory issues.
    """
    if not sqlite_db_path.endswith(".db"):
        sqlite_db_path = "{}.db".format(sqlite_db_path)
    # Create a connection to the SQLite database
    conn = sqlite3.connect(sqlite_db_path)
    if verbose:
        print(f"[+] Importing {csv_file_path} into SQLite database {sqlite_db_path}...")

    # Iterate over the CSV file in chunks
    for chunk in pd.read_csv(csv_file_path, chunksize=chunksize, sep=separator):
        # Append each chunk to the specified table in the SQLite database
        chunk.to_sql(name=table_name, con=conn, if_exists='replace', index=False)

    if verbose:
        print(f"[+] Database {sqlite_db_path} with table {table_name} created succesfully !")

    # Close the connection to the SQLite database
    conn.close()


def prepare_database(database, verbose):
    """
    Prepare the database by creating necessary indexes to improve query performance.
    """
    if not database.endswith(".db"):
        database = "{}.db".format(database)
    try:
        if verbose:
            print("[+] Optimize database...")
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("""CREATE INDEX IF NOT EXISTS "address_index" ON "addresses" ( "numero", "rep", 
                "nom_voie", "code_postal", "nom_commune" )""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS "numero_index" ON "addresses" ("numero")""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS "rep_index" ON "addresses" ("rep")""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS "nom_voie_index" ON "addresses" ("nom_voie")""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS "code_postal_index" ON "addresses" ("code_postal")""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS "nom_commune_index" ON "addresses" ("nom_commune")""")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if verbose:
            print(f"[+] Indexes in {database} was created succesfully !")
        conn.close()
