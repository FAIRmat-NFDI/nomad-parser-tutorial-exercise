import numpy as np

# Physical constants (CODATA 2018)
_H = 6.62607015e-34  # J·s
_C = 2.99792458e8  # m/s
_KB = 1.380649e-23  # J/K
_WIEN_B = 2.897771955e-3  # m·K  (Wien's displacement constant)


def planck_spectrum(
    temperature: float,
    wavelength_min: float = 100.0,
    wavelength_max: float = 3000.0,
    n_points: int = 500,
) -> dict:
    """
    Compute the Planck spectral radiance B(λ, T) over a wavelength range.

    Args:
        temperature:    Blackbody temperature in Kelvin.
        wavelength_min: Start of wavelength range in nm. Defaults to 100 nm.
        wavelength_max: End of wavelength range in nm. Defaults to 3000 nm.
        n_points:       Number of wavelength points. Defaults to 500.

    Returns:
        dict with keys:
            'wavelength'        - wavelength array in nm  (list[float])
            'spectral_radiance' - B(λ,T) in W·sr⁻¹·m⁻³  (list[float])
            'peak_wavelength'   - λ_max from Wien's law in nm (float)
    """
    if temperature <= 0:
        raise ValueError('Temperature must be greater than zero.')
    if wavelength_min <= 0 or wavelength_max <= 0:
        raise ValueError('Wavelength bounds must be greater than zero.')
    if wavelength_min >= wavelength_max:
        raise ValueError('wavelength_min must be less than wavelength_max.')
    if n_points <= 1:
        raise ValueError('n_points must be greater than 1.')

    lam_nm = np.linspace(wavelength_min, wavelength_max, n_points)
    lam_m = lam_nm * 1e-9

    exponent = (_H * _C) / (lam_m * _KB * temperature)
    spectral_radiance = (2 * _H * _C**2 / lam_m**5) / (np.exp(exponent) - 1)
    peak_wavelength_nm = (_WIEN_B / temperature) * 1e9

    return {
        'wavelength': lam_nm.tolist(),
        'spectral_radiance': spectral_radiance.tolist(),
        'peak_wavelength': peak_wavelength_nm,
    }
