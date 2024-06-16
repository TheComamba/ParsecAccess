use serde::{Deserialize, Serialize};
use simple_si_units::base::{Mass, Time};
use std::ops::Index;

use super::line::ParsedParsecLine;

#[derive(Deserialize, Serialize, Clone)]
pub(super) struct Trajectory {
    params: Vec<ParsedParsecLine>,
    pub(super) initial_mass: Mass<f64>,
    pub(super) lifetime: Time<f64>,
}

impl Index<usize> for Trajectory {
    type Output = ParsedParsecLine;

    fn index(&self, index: usize) -> &Self::Output {
        &self.params[index]
    }
}

impl Trajectory {
    pub(super) const EMPTY: Trajectory = Trajectory {
        params: Vec::new(),
        initial_mass: Mass { kg: 0. },
        lifetime: Time { s: 0. },
    };

    pub(super) fn new(params: Vec<ParsedParsecLine>) -> Self {
        let initial_mass = Mass::from_solar_mass(params[0].mass_in_solar_masses);
        let lifetime = match params.last() {
            Some(last) => Time::from_yr(last.age_in_years),
            None => Time { s: 0. },
        };

        Self {
            params,
            initial_mass,
            lifetime,
        }
    }

    pub(super) fn get_params_by_index(&self, index: usize) -> Option<&ParsedParsecLine> {
        self.params.get(index)
    }

    pub(super) fn get_params_by_index_unchecked(&self, index: usize) -> &ParsedParsecLine {
        &self.params[index]
    }

    pub(super) fn get_closest_params_index(&self, actual_age_in_years: f64) -> usize {
        if actual_age_in_years < self.params[0].age_in_years {
            return Self::this_or_next_age_index(self, 0, actual_age_in_years);
        }

        let mut age_index = 1;
        while self.params[age_index].age_in_years < actual_age_in_years {
            age_index *= 2;
            if age_index >= self.params.len() {
                age_index = self.params.len() - 2;
                break;
            }
        }

        while self.params[age_index].age_in_years > actual_age_in_years {
            age_index -= 1;
        }

        Self::this_or_next_age_index(self, age_index, actual_age_in_years)
    }

    fn this_or_next_age_index(&self, age_index: usize, actual_age_in_years: f64) -> usize {
        let this_age = self.params[age_index].age_in_years;
        let diff_to_this = actual_age_in_years - this_age;
        let next_age = self.params[age_index + 1].age_in_years;
        let diff_to_next = next_age - actual_age_in_years;
        if diff_to_this <= diff_to_next {
            age_index
        } else {
            age_index + 1
        }
    }

    #[cfg(test)]
    pub(super) fn get_params(&self) -> &Vec<ParsedParsecLine> {
        &self.params
    }

    pub(super) fn is_empty(&self) -> bool {
        self.params.is_empty()
    }
}
