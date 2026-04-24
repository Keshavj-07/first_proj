import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    sigma2 = (1e4/wavelength_air)**2.
    fact = 1.0 + 5.792105e-2/(238.0185 - sigma2) + 1.67917e-3/(57.362 - sigma2)

    return wavelength_air * fact

def bass_compare(obs_x, obs_y, sim_x, sim_y, x_min=6061, x_max=7061):
    """
    Compare the observed solar spectrum with the STARDIS simulation
    Parameters
    -----------
    wavelength: array-like
        Wavelengths of the stardis solar spectrum in Angstroms
    flux: array-like
        Flux densities of the stardis solar spectrum in erg/s/cm^2/Angstrom

    Returns
    --------
    None
    """
    plt.figure(figsize=(10,6))
    plt.plot(obs_x, obs_y, label='Observed Solar Spectrum', color = 'black', alpha = 0.6)
    plt.xlim((x_min, x_max))
    plt.title("Observation vs STARDIS Solar Spectrum")
    plt.xlabel(r"Wavelength [$\AA$]")
    plt.ylabel(r"Flux density [erg/s/cm$^2$/$\AA$]")
    plt.tight_layout()

    plt.plot (sim_x, sim_y, label='STARDIS Simulation')
    #plt.vlines(6564.6, ymin=0, ymax=10000, color='red', label='H-alpha line')
    #plt.vlines(6867.4, ymin=0, ymax=10000, color='red', label='O2 B line')
    plt.legend()
    plt.show()


def continuum_visualizer(x1, y1, x2, y2, x_min=6061, x_max=7061):
    """
    Visualize the continuum of the STARDIS simulation
    Parameters
    -----------
    wavelength: array-like
        Wavelengths of the stardis solar spectrum in Angstroms
    flux: array-like
        Flux densities of the stardis solar spectrum in erg/s/cm^2/Angstrom

    Returns
    --------
    None
    """
    plt.figure(figsize=(10,6))
    plt.plot(x2, y2, label='STARDIS Simulation')
    plt.xlim((x_min, x_max))
    plt.title("STARDIS Solar Spectrum Continuum")
    plt.xlabel(r"Wavelength [$\AA$]")
    plt.ylabel(r"Flux density [erg/s/cm$^2$/$\AA$]")
    plt.tight_layout()

    plt.plot (x1, y1, label='Continuum', color='red')
    plt.legend()
    plt.show()