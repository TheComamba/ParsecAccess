// This code is generated by generate_code.py, do not modify it manually.

//! Provides access to the data files for the PARSEC stellar evolution models.

use lazy_static::lazy_static;
use serde::{Deserialize, Serialize};
use std::ops::Index;
use std::sync::Mutex;

use crate::{error::ParsecAccessError, trajectory::Trajectory};

use super::metallicity::Metallicity;

lazy_static! {
    static ref Z0_0001_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0002_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0005_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0010_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0020_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0040_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0060_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0080_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0100_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0140_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0170_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0200_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0300_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0400_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
    static ref Z0_0600_DATA: Mutex<Result<ParsecData, ParsecAccessError>> =
        Mutex::new(ParsecData::new());
}

static DATA: [&Mutex<Result<ParsecData, ParsecAccessError>>; 15] = [
    &Z0_0001_DATA,
    &Z0_0002_DATA,
    &Z0_0005_DATA,
    &Z0_0010_DATA,
    &Z0_0020_DATA,
    &Z0_0040_DATA,
    &Z0_0060_DATA,
    &Z0_0080_DATA,
    &Z0_0100_DATA,
    &Z0_0140_DATA,
    &Z0_0170_DATA,
    &Z0_0200_DATA,
    &Z0_0300_DATA,
    &Z0_0400_DATA,
    &Z0_0600_DATA,
];

#[derive(Deserialize, Serialize)]
pub(crate) struct ParsecData {
    pub metallicity: Metallicity,
    pub(super) data: Vec<Trajectory>,
}

impl Index<usize> for ParsecData {
    type Output = Trajectory;

    fn index(&self, index: usize) -> &Self::Output {
        &self.data[index]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[ignore]
    fn data_access_is_fast() {
        const N: usize = 1000;
        const PRIME1: usize = 1009;
        const PRIME2: usize = 1013;
        const PRIME3: usize = 10007;
        const MAX_METALLICITY_INDEX: usize = 10;
        const MAX_MASS_INDEX: usize = 50;
        const MAX_TRAJECTORY_INDEX: usize = 1000;

        // Ensure that the data is loaded into memory.
        for i in 0..N {
            let _ = DATA[i][1][1];
        }

        // Create pseudo-random indices.
        let mut indices = Vec::new();
        for i in 0..N {
            let metallicity_index = (i * PRIME1) % MAX_METALLICITY_INDEX;
            let mass_index = (i * PRIME2) % MAX_MASS_INDEX;
            let trajectory_index = (i * PRIME3) % MAX_TRAJECTORY_INDEX;
            indices.push((metallicity_index, mass_index, trajectory_index));
        }

        // Access the data in a pseudo-random order.
        let now = std::time::Instant::now();
        for (metallicity_index, mass_index, trajectory_index) in indices {
            let _ = DATA[metallicity_index][mass_index][trajectory_index];
        }
        let elapsed = now.elapsed();

        println!("Accessing {} data points took {:?}", N, elapsed);
    }
}
