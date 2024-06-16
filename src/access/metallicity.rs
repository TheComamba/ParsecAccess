// This code is generated by generate_code.py, do not modify it manually.

enum Metallicity {
    /// Metallic mass fraction Z = 0.0001
    Z0p0001,
    /// Metallic mass fraction Z = 0.0002
    Z0p0002,
    /// Metallic mass fraction Z = 0.0005
    Z0p0005,
    /// Metallic mass fraction Z = 0.0010
    Z0p0010,
    /// Metallic mass fraction Z = 0.0020
    Z0p0020,
    /// Metallic mass fraction Z = 0.0040
    Z0p0040,
    /// Metallic mass fraction Z = 0.0060
    Z0p0060,
    /// Metallic mass fraction Z = 0.0080
    Z0p0080,
    /// Metallic mass fraction Z = 0.0100
    Z0p0100,
    /// Metallic mass fraction Z = 0.0140
    Z0p0140,
    /// Metallic mass fraction Z = 0.0170
    Z0p0170,
    /// Metallic mass fraction Z = 0.0200
    Z0p0200,
    /// Metallic mass fraction Z = 0.0300
    Z0p0300,
    /// Metallic mass fraction Z = 0.0400
    Z0p0400,
    /// Metallic mass fraction Z = 0.0600
    Z0p0600,
}

impl Metallicity {
    fn to_archive_name(&self) -> &str {
        match self {
            Metallicity::Z0p0001 => "Z0.0001Y0.249.tar.gz",
            Metallicity::Z0p0002 => "Z0.0002Y0.249.tar.gz",
            Metallicity::Z0p0005 => "Z0.0005Y0.249.tar.gz",
            Metallicity::Z0p0010 => "Z0.001Y0.25.tar.gz",
            Metallicity::Z0p0020 => "Z0.002Y0.252.tar.gz",
            Metallicity::Z0p0040 => "Z0.004Y0.256.tar.gz",
            Metallicity::Z0p0060 => "Z0.006Y0.259.tar.gz",
            Metallicity::Z0p0080 => "Z0.008Y0.263.tar.gz",
            Metallicity::Z0p0100 => "Z0.01Y0.267.tar.gz",
            Metallicity::Z0p0140 => "Z0.014Y0.273.tar.gz",
            Metallicity::Z0p0170 => "Z0.017Y0.279.tar.gz",
            Metallicity::Z0p0200 => "Z0.02Y0.284.tar.gz",
            Metallicity::Z0p0300 => "Z0.03Y0.302.tar.gz",
            Metallicity::Z0p0400 => "Z0.04Y0.321.tar.gz",
            Metallicity::Z0p0600 => "Z0.06Y0.356.tar.gz",
        }
    }

    fn to_mass_fraction(&self) -> f32 {
        match self {
            Metallicity::Z0p0001 => 0.0001,
            Metallicity::Z0p0002 => 0.0002,
            Metallicity::Z0p0005 => 0.0005,
            Metallicity::Z0p0010 => 0.001,
            Metallicity::Z0p0020 => 0.002,
            Metallicity::Z0p0040 => 0.004,
            Metallicity::Z0p0060 => 0.006,
            Metallicity::Z0p0080 => 0.008,
            Metallicity::Z0p0100 => 0.01,
            Metallicity::Z0p0140 => 0.014,
            Metallicity::Z0p0170 => 0.017,
            Metallicity::Z0p0200 => 0.02,
            Metallicity::Z0p0300 => 0.03,
            Metallicity::Z0p0400 => 0.04,
            Metallicity::Z0p0600 => 0.06,
        }
    }

    fn find_closest_from_mass_fraction(mass_fraction: f32) -> Metallicity {
        if mass_fraction < 0.00015000000000000001 {
            return Z0p0001;
        }
        if mass_fraction < 0.00035 {
            return Z0p0002;
        }
        if mass_fraction < 0.00075 {
            return Z0p0005;
        }
        if mass_fraction < 0.0015 {
            return Z0p0010;
        }
        if mass_fraction < 0.003 {
            return Z0p0020;
        }
        if mass_fraction < 0.005 {
            return Z0p0040;
        }
        if mass_fraction < 0.007 {
            return Z0p0060;
        }
        if mass_fraction < 0.009000000000000001 {
            return Z0p0080;
        }
        if mass_fraction < 0.012 {
            return Z0p0100;
        }
        if mass_fraction < 0.0155 {
            return Z0p0140;
        }
        if mass_fraction < 0.018500000000000003 {
            return Z0p0170;
        }
        if mass_fraction < 0.025 {
            return Z0p0200;
        }
        if mass_fraction < 0.035 {
            return Z0p0300;
        }
        if mass_fraction < 0.05 {
            return Z0p0400;
        }
        return Z0p0600;
    }

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
    fn to_fe_dex(self) -> f32 {
        match self {
            Metallicity::Z0p0001 => -2.0863598306747484,
            Metallicity::Z0p0002 => -1.7853298350107671,
            Metallicity::Z0p0005 => -1.3873898263387294,
            Metallicity::Z0p0010 => -1.0863598306747484,
            Metallicity::Z0p0020 => -0.7853298350107671,
            Metallicity::Z0p0040 => -0.4842998393467859,
            Metallicity::Z0p0060 => -0.3082085802911046,
            Metallicity::Z0p0080 => -0.1832698436828047,
            Metallicity::Z0p0100 => -0.08635983067474828,
            Metallicity::Z0p0140 => 0.059768205003489776,
            Metallicity::Z0p0170 => 0.14408909070352569,
            Metallicity::Z0p0200 => 0.21467016498923291,
            Metallicity::Z0p0300 => 0.39076142404491415,
            Metallicity::Z0p0400 => 0.5157001606532141,
            Metallicity::Z0p0600 => 0.6917914197088953,
        }
    }

    fn find_closest_from_fe_dex(fe_dex: f32) -> Metallicity {
        if fe_dex < -1.9358448328427578 {
            return Z0p0001;
        }
        if fe_dex < -1.5863598306747484 {
            return Z0p0002;
        }
        if fe_dex < -1.236874828506739 {
            return Z0p0005;
        }
        if fe_dex < -0.9358448328427578 {
            return Z0p0010;
        }
        if fe_dex < -0.6348148371787765 {
            return Z0p0020;
        }
        if fe_dex < -0.3962542098189452 {
            return Z0p0040;
        }
        if fe_dex < -0.24573921198695464 {
            return Z0p0060;
        }
        if fe_dex < -0.1348148371787765 {
            return Z0p0080;
        }
        if fe_dex < -0.013295812835629254 {
            return Z0p0100;
        }
        if fe_dex < 0.10192864785350773 {
            return Z0p0140;
        }
        if fe_dex < 0.17937962784637929 {
            return Z0p0170;
        }
        if fe_dex < 0.30271579451707353 {
            return Z0p0200;
        }
        if fe_dex < 0.45323079234906416 {
            return Z0p0300;
        }
        if fe_dex < 0.6037457901810548 {
            return Z0p0400;
        }
        return Z0p0600;
    }
}
