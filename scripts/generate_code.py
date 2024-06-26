
from bs4 import BeautifulSoup # Pulling data out of HTML and XML files
import glob # Unix style pathname pattern expansion
import math
import os
import re # Regular Expressions
import requests
import tarfile

URL = "https://people.sissa.it/~sbressan/CAF09_V1.2S_M36_LT/"

TARGET_DIR = "src/access/"

MOD_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

pub(crate) const PARSEC_URL: &str = "{URL}";

pub(crate) mod data;
pub(crate) mod metallicity;
pub(crate) mod masses;
"""

DATA_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

use lazy_static::lazy_static;

use crate::data::ParsecData;

lazy_static! {{
    {static_data}
}}

lazy_static! {{
    pub(crate) static ref DATA: [&'static ParsecData; {array_size}] = [
        {access_array}
    ];
}}
"""

METALLICITY_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

pub(crate) static METALLICITIES_IN_MASS_FRACTION: [f64; {number_of_metallicities}] = [
    {mass_fraction_array}
];

pub(crate) static METALLICITIES_IN_DEX: [f64; {number_of_metallicities}] = [
    {dex_array}
];

pub(crate) static METALLICITY_NAMES: [&str; {number_of_metallicities}] = [
    {names_array}
];

/// Using this, the crate knows which file to download during intialisation.
pub(crate) static METALLICITY_ARCHIVES: [&str; {number_of_metallicities}] = [
    {archives_array}
];
"""

MASSES_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

{sorted_masses}

{filenames}

pub(crate) static MASSES: [&[f64]; {number_of_metallicities}] = [
        {metallicity_to_masses}
];

pub(crate) static FILENAMES: [&[&str]; {number_of_metallicities}] = [
        {metallicity_to_filenames}
];
"""

def assure_dev_data_folder():
    if not os.path.exists('dev_data'):
        os.makedirs('dev_data')

def collect_archive_names():
    FILE_PATH = "dev_data/archive_names.html"
    if not os.path.isfile(FILE_PATH):
        web_page = requests.get(URL).text
        with open(FILE_PATH, 'w') as file:
            file.write(web_page)

    with open(FILE_PATH, 'r') as file:
        web_page = file.read()

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

def normalised_metallicity_string(metallicity):
    if not metallicity.startswith("0."):
        metallicity = "0." + metallicity
    metallicity_float = float(metallicity)
    return "{:.4f}".format(metallicity_float)

def create_map_from_metallicity_to_archive_name(archive_names):
    map = {}
    metallicities = []
    for archive_name in archive_names:
        if archive_name.endswith('.tar.gz'):
            match = re.search('Z(.*?)Y', archive_name)
            metallicity = normalised_metallicity_string(match.group(1))
            map[metallicity] = archive_name
            metallicities.append(metallicity)
    metallicities.sort()
    return map, metallicities

def collect_mass_filenames(archive_name):
    dir_name = 'dev_data/' + archive_name.replace('.tar.gz', '')
    files = glob.glob(os.path.join(dir_name, '*.DAT'))
    return files

def normalised_mass_string(mass):
    mass_float = float(mass)
    return "{:07.3f}".format(mass_float)

def create_map_from_mass_to_filename(filenames):
    map = {}
    masses = []
    for file in filenames:
        match = re.search('M(.*?).DAT', file)
        mass = normalised_mass_string(match.group(1))
        map[mass] = file
        masses.append(mass)
    masses.sort()
    return map, masses

def clean_target_dir():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    for file in os.listdir(TARGET_DIR):
        os.remove(TARGET_DIR + file)

def generate_mod_file():
    with open(TARGET_DIR + "mod.rs", 'w') as f:
        f.write(MOD_TEMPLATE.format(URL=URL))

def generate_data_file(metallicities):
    static_data = ""
    access_array = ""
    for index, metallicity in enumerate(metallicities):
        variant_name = metallicity_variant_name(metallicity)
        static_data += f"static {variant_name}_DATA: ParsecData = ParsecData::new({index});\n"
        access_array += f"&{variant_name}_DATA,\n"

    with open(TARGET_DIR + "data.rs", 'w') as f:
        f.write(DATA_TEMPLATE.format(static_data=static_data, 
                                     array_size=len(metallicities),
                                     access_array=access_array))

def mass_fraction_to_dex(mass_fraction):
    Z_sun = 0.0122
    return math.log10(mass_fraction / Z_sun)

def metallicity_variant_name(metallicity):
    return "Z" + metallicity.replace(".", "_")

def generate_metallicity_file(metallicities, metallicity_to_archive_name):
    mass_fraction_array = ""
    dex_array = ""
    names_array = ""
    array_str = ""
    archives_array = ""
    to_mass_fraction_str = ""
    to_dex_str = ""
    for metallicity in metallicities:
        variant_name = metallicity_variant_name(metallicity)
        mass_fraction = float(metallicity)
        dex = mass_fraction_to_dex(mass_fraction)
        mass_fraction_array += f"{mass_fraction},\n"
        dex_array += f"{dex},\n"
        archive_name = metallicity_to_archive_name[metallicity]

        names_array += f"\"{variant_name}\",\n"
        archives_array += f"\"{archive_name}\",\n"
        to_mass_fraction_str += f"Metallicity::{variant_name} => {mass_fraction},\n"
        to_dex_str += f"Metallicity::{variant_name} => {dex},\n"

    with open(TARGET_DIR + "metallicity.rs", 'w') as f:
        f.write(METALLICITY_TEMPLATE.format(number_of_metallicities=len(metallicities),
                                            mass_fraction_array=mass_fraction_array,
                                            dex_array=dex_array,
                                            names_array=names_array,
                                            archives_array=archives_array,
                                            metallicity_to_mass_fraction=to_mass_fraction_str,
                                            metallicity_to_dex=to_dex_str))

def generate_masses_constant(metallicity, masses):
    masses_str = f"const {metallicity_variant_name(metallicity)}_SORTED_MASSES: [f64; {len(masses)}] = ["
    for mass in masses:
        masses_str += f"{mass}, "
    masses_str += "];"
    return masses_str

def generate_filename_constant(metallicity, masses, mass_to_filename):
    filenames_str = f"const {metallicity_variant_name(metallicity)}_FILENAMES: [&str; {len(masses)}] = ["
    for mass in masses:
        filename = os.path.basename(mass_to_filename[mass])
        filenames_str += f"\"{filename}\", "
    filenames_str += "];"
    return filenames_str

def generate_masses_file(metallicities, metallicity_to_masses, metallicity_and_mass_to_filename):
    sorted_masses = ""
    filenames = ""
    metallicity_to_masses_str = ""
    metallicity_to_filenames_str = ""
    for metallicity in metallicities:
        masses = metallicity_to_masses[metallicity]
        sorted_masses += generate_masses_constant(metallicity, masses) + "\n"
        filenames += generate_filename_constant(metallicity, masses, metallicity_and_mass_to_filename[metallicity]) + "\n"
        metallicity_name = metallicity_variant_name(metallicity)
        metallicity_to_masses_str += f"&{metallicity_name}_SORTED_MASSES,\n"
        metallicity_to_filenames_str += f"&{metallicity_name}_FILENAMES,\n"

    with open(TARGET_DIR + "masses.rs", 'w') as f:
        f.write(MASSES_TEMPLATE.format(sorted_masses=sorted_masses,
                                        filenames=filenames,
                                        number_of_metallicities=len(metallicities),
                                        metallicity_to_masses=metallicity_to_masses_str,
                                        metallicity_to_filenames=metallicity_to_filenames_str))

def main():
    assure_dev_data_folder()
    archive_names = collect_archive_names()
    for archive_name in archive_names:
        assure_archive_downloaded(archive_name)
        assure_extracted(archive_name)
        delete_obsolete_files(archive_name)
    metallicity_to_archive_name, metallicities = create_map_from_metallicity_to_archive_name(archive_names)
    metallicity_and_mass_to_filename = {}
    metallicity_to_masses = {}
    for metallicity, archive_name in metallicity_to_archive_name.items():
        mass_filenames = collect_mass_filenames(archive_name)
        mass_to_filename, masses = create_map_from_mass_to_filename(mass_filenames)
        metallicity_and_mass_to_filename[metallicity] = mass_to_filename
        metallicity_to_masses[metallicity] = masses

    clean_target_dir()
    generate_mod_file()
    generate_data_file(metallicities)
    generate_metallicity_file(metallicities, metallicity_to_archive_name)
    generate_masses_file(metallicities, metallicity_to_masses, metallicity_and_mass_to_filename)

main()
