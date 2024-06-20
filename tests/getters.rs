#[cfg(test)]
mod tests {
    use parsec_access::getters::{
        get_ages_in_years, get_closest_age_index, get_closest_mass_index,
        get_closest_metallicity_index_from_mass_fraction, get_masses_in_solar,
        get_metallicities_in_mass_fractions,
    };
    use simple_si_units::base::{Mass, Time};

    #[test]
    fn metallicites_are_mapped_to_themselves() {
        for (expected_index, expected_value) in
            get_metallicities_in_mass_fractions().iter().enumerate()
        {
            let index = get_closest_metallicity_index_from_mass_fraction(*expected_value);
            assert_eq!(expected_index, index);
        }
    }

    #[test]
    fn masses_are_mapped_to_themselves() {
        let metallicity_index = 3;
        for (expected_index, expected_value) in
            get_masses_in_solar(metallicity_index).iter().enumerate()
        {
            let mass = Mass::from_solar_mass(*expected_value);
            let index = get_closest_mass_index(metallicity_index, mass);
            assert_eq!(expected_index, index);
        }
    }

    #[test]
    fn ages_are_mapped_to_themselves() {
        let metallicity_index = 3;
        let mass_index = 30;
        for (expected_index, expected_value) in get_ages_in_years(metallicity_index, mass_index)
            .iter()
            .enumerate()
        {
            let age = Time::from_yr(*expected_value);
            let index = get_closest_age_index(metallicity_index, mass_index, age);
            assert_eq!(expected_index, index);
        }
    }
}
