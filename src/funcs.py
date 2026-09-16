import matplotlib.pyplot as plt
import scipy.ndimage as nd
import numpy as np
from astropy import units as u
from stardis.base import run_stardis


def convert_wavelength_air2vacuum(wavelength_air):
    """
    Convert air wavelength to vacuum wavelength
    Parameters
    -----------
    wavelength_air: float
        Air wavelength in Angstroms

    Returns
    --------
    float
        Vacuum wavelength in Angstroms
    """
    sigma = (1e4 / wavelength_air) ** 2.0
    fact = 1.0 + 5.7921e-2 / (238.0185 - sigma) + 1.67917e-3 / (57.362 - sigma)

    return wavelength_air * fact


def bass_compare(obs_x, obs_y, sim_x, sim_y, start=6061, end=7061):
    """
    Compare the observed solar spectrum with the STARDIS simulation
    Parameters
    -----------
    obs_x: array-like
        Wavelengths of the observed spectrum in Angstroms
    obs_y: array-like
        Flux densities of the normalized observed spectrum
    sim_x: array-like
        Wavelengths of the stardis solar spectrum in Angstroms
    sim_y: array-like
        Flux densities of the stardis solar spectrum in erg/s/cm^2/Angstrom
    start: Float
        Starting wavelength value
    end: Float
        Ending wavelength value
    Returns
    --------
    None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(
        obs_x,
        obs_y,
        label="Observed Solar Spectrum",
        color="black",
        alpha=0.6,
    )
    plt.plot(
        sim_x,
        sim_y,
        label="STARDIS Simulation",
        color="tab:blue",
    )
    plt.xlim(start, end)
    plt.title("Stardis Solar Spectrum")
    plt.xlabel(r"Wavelength [$\AA$]")
    plt.ylabel(r"Flux density [erg/s/cm$^2$/$\AA$]")
    plt.tight_layout()
    # plt.vlines(6564.6, ymin=0, ymax=10000, color='red', label='H-alpha line')
    # plt.vlines(6867.4, ymin=0, ymax=10000, color='red', label='O2 B line')
    # plt.vlines(6282.6, ymin=0, ymax=10000, color='red', label='O2 A line')
    plt.vlines(7775.2, ymin=0, ymax=10000, color='red', label='OI Triplet')
    plt.legend()
    plt.show()


def continuum_visualizer(x1, y1, x2, y2):
    """
    Visualize the continuum of the STARDIS simulation
    Parameters
    -----------
    x1: array-like
        Wavelengths of the stardis solar spectrum in Angstroms
    y1: array-like
        Flux densities of the stardis solar spectrum in erg/s/cm^2/Angstrom
    x2: array-like
        Wavelengths of the stardis continuum in Angstroms
    y2: array-like
        Value for the continuum
    Returns
    --------
    None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x1, y1, label="STARDIS Simulation", color="tab:blue")
    plt.plot(x2, y2, label="Continuum", color="red")
    plt.title("STARDIS Solar Spectrum Continuum")
    plt.xlabel(r"Wavelength [$\AA$]")
    plt.ylabel(r"Flux density [erg/s/cm$^2$/$\AA$]")
    plt.tight_layout()
    plt.legend()
    plt.show()


def show_plots(obs_x, obs_y, sim, sim_nolines, factor=9932, sigma_pix=42.5):
    """
    Visualize the graph of a STARDIS simulation
    Parameters
    -----------
    obs_x: array-like
        Wavelengths of the observed spectrum in Angstroms
    obs_y: array-like
        Flux densities of the normalized observed spectrum
    sim: array-like
        Stardis solar spectrum simulation
    sim_nolines: array-like
        Stardis solar spectrum simulation without lines
    factor:
        Factor for normalizing spectrum
    Returns
    --------
    None
    """
    y_norm = sim.spectrum_lambda / sim_nolines.spectrum_lambda * factor
    continuum_visualizer(
        sim.lambdas,
        sim.spectrum_lambda,
        sim_nolines.lambdas,
        sim_nolines.spectrum_lambda,
    )
    convolved_flux = nd.gaussian_filter1d(y_norm, sigma_pix)
    bass_compare(obs_x, obs_y, sim.lambdas, convolved_flux, 6510, 6620)
    return convolved_flux


def simulation(file_main, file_nolines, obs_w_lambda, delta_lambda=0.1, n_factor=10000, start=6061, end=7061):
    """
    Run STARdis simulations with and without spectral lines.

    The two simulated spectra are divided to normalize the line spectrum,
    scaled by ``n_factor``, and convolved with a Gaussian representing the
    observed wavelength resolution.

    Parameters
    ----------
    file_main : path-like
        Stardis configuration file for the simulation.
    file_nolines : path-like
        Stardis configuration file for the continuum-only simulation.
    obs_w_lambda : astropy.units.Quantity
        Observed wavelength resolution, including its wavelength unit.
    delta_lambda : float
        Wavelength-grid spacing in Angstroms.
    n_factor : float
        Scaling factor applied to the normalized spectrum.
    start : float
        Starting wavelength of the simulation in Angstroms.
    end : float
        Ending wavelength of the simulation in Angstroms.

    Returns
    -------
    tuple
        The convolved normalized flux and the Stardis wavelength grid.
    """
    sim_delta_lambda = delta_lambda * u.Angstrom

    tracing_wavelengths = np.mgrid[start:end:delta_lambda] * u.Angstrom
    sim_full = run_stardis(file_main, tracing_wavelengths)
    sim_nolines = run_stardis(file_nolines, tracing_wavelengths)

    sim_normalized_flux = sim_full.spectrum_lambda/sim_nolines.spectrum_lambda * n_factor

    obs_sigma_lambda = obs_w_lambda/2.355
    obs_sigma_pix = obs_sigma_lambda/sim_delta_lambda
    sim_con_flux = nd.gaussian_filter1d(sim_normalized_flux, obs_sigma_pix)

    return sim_con_flux, sim_full.lambdas
