import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from astropy import units as u
from src.funcs import (simulation)
from stardis.base import run_stardis
from pathlib import Path

# Parameter-study simulations
obs_wavelength = 4.08 * u.Angstrom
start_wavelength = 22000
end_wavelength = 22100

# Defines a basic list of regular simulation files
regular_files = [
    "para_yml/2800K_marcs.yml",
    "para_yml/3000K_marcs.yml",
    "para_yml/3200K_marcs.yml",
    "para_yml/0_5m_marcs.yml",
    "para_yml/1m_marcs.yml",
    "para_yml/2m_marcs.yml",
    "para_yml/minus1_MH_marcs.yml",
    "para_yml/0_MH_marcs.yml",
    "para_yml/1_MH_marcs.yml",
    "para_yml/t1_marcs.yml",
    "para_yml/t2_marcs.yml",
    "para_yml/t5_marcs.yml",
]

# Defines other lists that use suffixes on the base list
nolines_files = [f.replace("_marcs.yml", "_nolines_marcs.yml") for f in regular_files]
asplund_files = [f.replace("_marcs.yml", "_asplund.yml") for f in regular_files]
asplund_nolines_files = [f.replace("_asplund.yml", "_nolines_asplund.yml") for f in asplund_files]

sim_dict = {}
# Marcs files simulation
for regular_file, nolines_file in zip(regular_files, nolines_files):
    name = "sim_" + Path(regular_file).stem
    sim_dict[name] = simulation(regular_file, nolines_file, obs_wavelength, start=start_wavelength, end=end_wavelength)

# Asplund files simulation
for regular_file, nolines_file in zip(asplund_files, asplund_nolines_files):
    name = "sim_" + Path(regular_file).stem 
    sim_dict[name] = simulation(regular_file, nolines_file, obs_wavelength, start=start_wavelength, end=end_wavelength)
fig, axes = plt.subplots(2, 2, figsize=(12, 10), sharex=True, sharey=True)

plots_asplund = [
    (axes[0, 0], sim_dict["sim_2800K_asplund"], "2800 K (Asplund)"),
    (axes[0, 0], sim_dict["sim_3000K_asplund"], "3000 K (Asplund)"),
    (axes[0, 0], sim_dict["sim_3200K_asplund"], "3200 K (Asplund)"),
    (axes[0, 1], sim_dict["sim_0_5m_asplund"], "0.5 m (Asplund)"),
    (axes[0, 1], sim_dict["sim_1m_asplund"], "1 m (Asplund)"),
    (axes[0, 1], sim_dict["sim_2m_asplund"], "2 m (Asplund)"),
    (axes[1, 0], sim_dict["sim_minus1_MH_asplund"], "-1 [M/H] (Asplund)"),
    (axes[1, 0], sim_dict["sim_0_MH_asplund"], "0 [M/H] (Asplund)"),
    (axes[1, 0], sim_dict["sim_1_MH_asplund"], "1 [M/H] (Asplund)"),
    (axes[1, 1], sim_dict["sim_t1_asplund"], "t = 1 (Asplund)"),
    (axes[1, 1], sim_dict["sim_t2_asplund"], "t = 2 (Asplund)"),
    (axes[1, 1], sim_dict["sim_t5_asplund"], "t = 5 (Asplund)"),
]

plots_marcs = [    
    (axes[0, 0], sim_dict["sim_2800K_marcs"], "2800 K (MARCS)"),
    (axes[0, 0], sim_dict["sim_3000K_marcs"], "3000 K (MARCS)"),
    (axes[0, 0], sim_dict["sim_3200K_marcs"], "3200 K (MARCS)"),
    (axes[0, 1], sim_dict["sim_0_5m_marcs"], "0.5 m (MARCS)"),
    (axes[0, 1], sim_dict["sim_1m_marcs"], "1 m (MARCS)"),
    (axes[0, 1], sim_dict["sim_2m_marcs"], "2 m (MARCS)"),
    (axes[1, 0], sim_dict["sim_minus1_MH_marcs"], "-1 [M/H] (MARCS)"),
    (axes[1, 0], sim_dict["sim_0_MH_marcs"], "0 [M/H] (MARCS)"),
    (axes[1, 0], sim_dict["sim_1_MH_marcs"], "1 [M/H] (MARCS)"),
    (axes[1, 1], sim_dict["sim_t1_marcs"], "t = 1 (MARCS)"),
    (axes[1, 1], sim_dict["sim_t2_marcs"], "t = 2 (MARCS)"),
    (axes[1, 1], sim_dict["sim_t5_marcs"], "t = 5 (MARCS)"),
]

line_markers = [
    (22026, "CN 1"),
    (22075.5, "CN 1"),
    (22038, "CN 0"),
    (22030, "Sc"),
    (22058.9, "Sc"),
    (22071, "Sc"),
    (22069, "Si"),
    (22079, "Si"),
    (22062, "Na"),
]

for axis, sim, title in plots_asplund:
    axis.plot(sim[1], sim[0], drawstyle="steps", label=title)

for axis, sim, title in plots_marcs:
    axis.plot(sim[1], sim[0], drawstyle="steps", label=title, linestyle="--")

for ax in axes.flat:
    ax.set_xlabel(r"Wavelength [$\AA$]")
    ax.set_ylabel("Normalized Flux")
    ax.legend(loc = 'lower left')
    ax.set_xlim(22020, 22080)
    for line_wavelength, label in line_markers:
        ax.axvline(line_wavelength, color="gray", linestyle="--", linewidth=0.8)
        ax.text(
            line_wavelength,
            0.1,
            label,
            transform=ax.get_xaxis_transform(),
            rotation=90,
            va="center",
            ha="right",
            fontsize=8,
        )


axes[0, 0].set_title("Temperature")
axes[0, 1].set_title("Mass")
axes[1, 0].set_title("Metallicity")
axes[1, 1].set_title("Microturbulence")

plt.tight_layout()
plt.show()