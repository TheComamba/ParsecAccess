
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

//! Provides access to an enum for the available metallicities, arrays of masses for each metallicity, and several helper functions.

pub(crate) mod data;
pub mod metallicity;
pub mod masses;
"""

DATA_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

//! Provides access to the data files for the PARSEC stellar evolution models.

use lazy_static::lazy_static;
use serde::{{Deserialize, Serialize}};
use std::ops::Index;
use std::sync::Mutex;

use crate::{{error::ParsecAccessError, trajectory::Trajectory}};

use super::metallicity::Metallicity;

lazy_static! {{
    {static_data}
}}

static DATA: [&Mutex<Result<ParsecData, ParsecAccessError>>; {array_size}] = [
    {access_array}
];

#[derive(Deserialize, Serialize)]
pub(crate) struct ParsecData {{
    pub metallicity: Metallicity,
    pub(super) data: Vec<Trajectory>,
}}

impl Index<usize> for ParsecData {{
    type Output = Trajectory;

    fn index(&self, index: usize) -> &Self::Output {{
        &self.data[index]
    }}
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    #[ignore]
    fn data_access_is_fast() {{
        const N: usize = 1000;
        const PRIME1: usize = 1009;
        const PRIME2: usize = 1013;
        const PRIME3: usize = 10007;
        const MAX_METALLICITY_INDEX: usize = 10;
        const MAX_MASS_INDEX: usize = 50;
        const MAX_TRAJECTORY_INDEX: usize = 1000;

        // Ensure that the data is loaded into memory.
        for i in 0..N {{
            let _ = DATA[i][1][1];
        }}

        // Create pseudo-random indices.
        let mut indices = Vec::new();
        for i in 0..N {{
            let metallicity_index = (i * PRIME1) % MAX_METALLICITY_INDEX;
            let mass_index = (i * PRIME2) % MAX_MASS_INDEX;
            let trajectory_index = (i * PRIME3) % MAX_TRAJECTORY_INDEX;
            indices.push((metallicity_index, mass_index, trajectory_index));
        }}

        // Access the data in a pseudo-random order.
        let now = std::time::Instant::now();
        for (metallicity_index, mass_index, trajectory_index) in indices {{
            let _ = DATA[metallicity_index][mass_index][trajectory_index];
        }}
        let elapsed = now.elapsed();

        println!("Accessing {{}} data points took {{:?}}", N, elapsed);
    }}
}}
"""

METALLICITY_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

//! Provides an enum for the available metallicities and several helper functions.

use serde::{{Deserialize, Serialize}};

/// Enum for the available metallicities.
/// The naming convention is Z followed by the metallicity in mass fraction, with the decimal point replaced by an underscore.
#[derive(Debug, Copy, Clone, PartialEq, Eq, Deserialize, Serialize)]
pub enum Metallicity {{
{metallicities}
}}

impl Metallicity {{
    /// Returns the name of the archive file for the metallicity.
    /// Using this, the crate knows which file to download during intialisation.
    fn to_archive_name(&self) -> &str {{
        match self {{
            {metallicity_to_archive_name}
        }}
    }}

    /// Converts the metallicity enum variant to the corresponding mass fraction Z.
    ///
    /// # Example
    /// ```
    /// use parsec_access::access::metallicity::Metallicity;
    ///
    /// let mass_fraction = Metallicity::Z0_0100.to_mass_fraction();
    /// assert!((mass_fraction - 0.01).abs() < 1e-10);
    /// ```
    pub fn to_mass_fraction(&self) -> f32 {{
        match self {{
            {metallicity_to_mass_fraction}
        }}
    }}

    /// Finds the closest metallicity enum variant to the given mass fraction Z.
    ///
    /// The midpoint between two metallicities is calculated as the arithmetic mean of the two mass fractions.
    /// Note that this means that there are cases where find_closest_from_fe_dex can lead to a different result.
    ///
    /// # Example
    /// ```
    /// use parsec_access::access::metallicity::Metallicity;
    ///
    /// let closest = Metallicity::find_closest_from_mass_fraction(0.0101);
    /// assert_eq!(closest, Metallicity::Z0_0100);
    /// let closest = Metallicity::find_closest_from_mass_fraction(0.);
    /// assert_eq!(closest, Metallicity::Z0_0001);
    /// let closest = Metallicity::find_closest_from_mass_fraction(0.999);
    /// assert_eq!(closest, Metallicity::Z0_0600);
    /// ```
    pub fn find_closest_from_mass_fraction(mass_fraction: f32) -> Metallicity {{
        {find_closest_mass_fraction}
    }}

    /// Converts the metallicity to units of dex for the element iron, using several assumptions.
    ///
    /// PARSEC lists metallicity as
    /// Z = m_M / m_tot ,
    /// the mass fraction of all metals (i.e. elements heavier than Helium) in the star.
    ///
    /// The chemical abundance ratio on the other hand is conventionally given as
    /// [Fe/H] = log10(N_Fe / N_H) - log10(N_Fe / N_H)_sun ,
    /// where N_Fe and N_H are the number densities of iron and hydrogen atoms, respectively.
    ///
    /// Assuming that iron always makes up more or less the same fraction of the total mass,
    /// N_Fe = a * m_M
    /// and that the total mass is dominated by hydrogen,
    /// N_H = m_tot ,
    /// we find
    /// [Fe/H] = log10(a * m_M / m_tot) - log10(a * m_M / m_tot)_sun
    ///        = log10(Z / Z_sun) .
    ///
    /// The solar metallicity is Z_sun = 0.0122.
    ///
    /// # Example
    /// ```
    /// use parsec_access::access::metallicity::Metallicity;
    ///
    /// let dex = Metallicity::Z0_0100.to_fe_dex();
    /// assert!((dex + 0.086).abs() < 1e-3);
    /// ```
    pub fn to_fe_dex(self) -> f32 {{
        match self {{
            {metallicity_to_dex}
        }}
    }}

    /// Finds the closest metallicity enum variant to the given dex for the element iron.
    ///
    /// The midpoint between two metallicities is calculated as the arithmetic mean of the two dex values.
    /// Note that this means that there are cases where find_closest_from_mass_fraction can lead to a different result.
    ///
    /// # Example
    /// ```
    /// use parsec_access::access::metallicity::Metallicity;
    ///
    /// let closest = Metallicity::find_closest_from_fe_dex(0.);
    /// assert_eq!(closest, Metallicity::Z0_0140, "The sun should have a metallicity of roughlty Z = 0.0122. The test found {{}}", closest.to_mass_fraction());
    /// let closest = Metallicity::find_closest_from_fe_dex(-10.);
    /// assert_eq!(closest, Metallicity::Z0_0001, "The lowest metallicity should be Z = 0.0001. The test found {{}}", closest.to_mass_fraction());
    /// let closest = Metallicity::find_closest_from_fe_dex(10.);
    /// assert_eq!(closest, Metallicity::Z0_0600, "The highest metallicity should be Z = 0.06. The test found {{}}", closest.to_mass_fraction());
    /// ```
    pub fn find_closest_from_fe_dex(fe_dex: f32) -> Metallicity {{
        {find_closest_dex}
    }}
}}

"""

MASSES_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

//! Provides access to arrays of masses for each metallicity.

use super::metallicity::Metallicity;

{sorted_masses}

{filenames}

/// Returns a reference to the sorted array of masses available for the given metallicity.
pub fn get_masses(metallicity: &Metallicity) -> &[f64] {{
    match metallicity {{
        {metallicity_to_masses}
    }}
}}

/// Returns a reference to the sorted array of filenames available for the given metallicity.
/// The files have the same order as the masses, and can thus be accessed via index.
fn get_filenames(metallicity: &Metallicity) -> &[&str] {{
    match metallicity {{
        {metallicity_to_filenames}
    }}
}}
"""

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
        f.write(MOD_TEMPLATE)

def generate_data_file(metallicities):
    static_data = ""
    access_array = ""
    for metallicity in metallicities:
        variant_name = metallicity_variant_name(metallicity)
        static_data += f"static {variant_name}_DATA:"
        static_data += "Mutex<Result<ParsecData, ParsecAccessError>> = "
        static_data += "Mutex::new(ParsecData::new());\n"
        access_array += f"&{variant_name}_DATA,\n"

    with open(TARGET_DIR + "data.rs", 'w') as f:
        f.write(DATA_TEMPLATE.format(static_data=static_data, 
                                     array_size=len(metallicities),
                                     access_array=access_array))

def mass_fraction_to_dex(mass_fraction):
    Z_sun = 0.0122
    return math.log10(mass_fraction / Z_sun)

def generate_find_closest_function(input_variable_name, variant_and_value_pairs):
    intermediate_values = []
    for i in range(len(variant_and_value_pairs) - 1):
        _variant, value = variant_and_value_pairs[i]
        _next_variant, next_value = variant_and_value_pairs[i + 1]
        intermediate_values.append((value + next_value) / 2)
    function_str = ""
    for i in range(len(variant_and_value_pairs)):
        variant, _value = variant_and_value_pairs[i]
        if i < len(variant_and_value_pairs) - 1:
            intermediate = intermediate_values[i]
            function_str += f"if {input_variable_name} < {intermediate} {{ return {variant}; }}\n"
        else:
            function_str += f"return {variant};\n"
    return function_str

def metallicity_variant_name(metallicity):
    return "Z" + metallicity.replace(".", "_")

def generate_metallicity_file(metallicities, metallicity_to_archive_name):
    enum_str = ""
    to_archive_str = ""
    to_mass_fraction_str = ""
    to_dex_str = ""
    metallicity_and_mass_fraction = []
    metallicity_and_dex = []
    for metallicity in metallicities:
        enum_comment = "/// Metallic mass fraction Z = " + metallicity
        variant_name = metallicity_variant_name(metallicity)
        archive_name = metallicity_to_archive_name[metallicity]
        mass_fraction = float(metallicity)
        metallicity_and_mass_fraction.append((f"Metallicity::{variant_name}", mass_fraction))
        dex = mass_fraction_to_dex(mass_fraction)
        metallicity_and_dex.append((f"Metallicity::{variant_name}", dex))

        enum_str += f"{enum_comment}\n{variant_name},\n"
        to_archive_str += f"Metallicity::{variant_name} => \"{archive_name}\",\n"
        to_mass_fraction_str += f"Metallicity::{variant_name} => {mass_fraction},\n"
        to_dex_str += f"Metallicity::{variant_name} => {dex},\n"
    find_closest_mass_fraction = generate_find_closest_function("mass_fraction", metallicity_and_mass_fraction)
    find_closest_dex = generate_find_closest_function("fe_dex", metallicity_and_dex)

    with open(TARGET_DIR + "metallicity.rs", 'w') as f:
        f.write(METALLICITY_TEMPLATE.format(metallicities=enum_str,
                                            metallicity_to_archive_name=to_archive_str,
                                            metallicity_to_mass_fraction=to_mass_fraction_str,
                                            find_closest_mass_fraction=find_closest_mass_fraction,
                                            metallicity_to_dex=to_dex_str,
                                            find_closest_dex=find_closest_dex))

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
        metallicity_to_masses_str += f"Metallicity::{metallicity_name} => &{metallicity_name}_SORTED_MASSES,\n"
        metallicity_to_filenames_str += f"Metallicity::{metallicity_name} => &{metallicity_name}_FILENAMES,\n"

    with open(TARGET_DIR + "masses.rs", 'w') as f:
        f.write(MASSES_TEMPLATE.format(sorted_masses=sorted_masses,
                                       filenames=filenames,
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

# TODO: Create a check for updates workflow
