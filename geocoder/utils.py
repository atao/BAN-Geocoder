import gzip
import shutil

import requests


def uncompress_gz_to_csv(gz_file_path, csv_file_path, verbose):
    """
    Uncompress a .gz file and write the contents to a .csv file.

    Parameters:
    - gz_file_path (str): The file path of the .gz file to uncompress.
    - csv_file_path (str): The file path where the .csv will be saved.
    """
    if verbose:
        print(f"[+] Uncompressing {gz_file_path} to {csv_file_path}")
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(csv_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_csv(url, output_path, verbose):
    """
    Download a CSV file from a given URL and save it to the specified path.

    Parameters:
    - url (str): The URL of the CSV file to download.
    - output_path (str): The file path where the CSV will be saved.
    """
    if verbose:
        print(f"[+] Downloading BAN datasheet from {url}")

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the response to a file
        with open(output_path, 'wb') as file:
            file.write(response.content)
        if verbose:
            print(f"[+] File downloaded successfully: {output_path}")
    else:
        print(f"[!] Failed to download CSV file. HTTP Status Code: {response.status_code}")
