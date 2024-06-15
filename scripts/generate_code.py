
from bs4 import BeautifulSoup
import glob
import os
import requests
import tarfile

URL = "https://people.sissa.it/~sbressan/CAF09_V1.2S_M36_LT/"

def assure_dev_data_folder():
    if not os.path.exists('dev_data'):
        os.makedirs('dev_data')

def collect_archive_names():
    web_page = requests.get(URL).text
    soup = BeautifulSoup(web_page, 'html.parser')
    archive_names = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.tar.gz'):
            archive_names.append(href)
    return archive_names

def assure_archive_downloaded(archive_name):
    archive_path = f'dev_data/{archive_name}'
    if not os.path.exists(archive_path):
        archive_url = f'{URL}{archive_name}'
        print(f'Downloading {archive_url}...')
        with requests.get(archive_url, stream=True) as r:
            with open(archive_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

def assure_extracted(archive_name):
    archive_path = f'dev_data/{archive_name}'
    extract_dir = 'dev_data'

    target_path = extract_dir + '/' + archive_name.replace('.tar.gz', '')
    if not os.path.exists(target_path):
        with tarfile.open(archive_path, 'r:gz') as tar:
            print(f'Extracting {archive_path}...')
            tar.extractall(path=extract_dir)

def delete_obsolete_files(archive_name):
    dir_name = 'dev_data/' + archive_name.replace('.tar.gz', '')
    files = glob.glob(os.path.join(dir_name, '*.HB.DAT'))
    for file in files:
        os.remove(file)
    files = glob.glob(os.path.join(dir_name, '*ADD.DAT'))
    for file in files:
        os.remove(file)

def main():
    assure_dev_data_folder()
    archive_names = collect_archive_names()
    archive_names.sort()
    for archive_name in archive_names:
        assure_archive_downloaded(archive_name)
        assure_extracted(archive_name)
        delete_obsolete_files(archive_name)

main()
