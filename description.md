# Introduction

Statistical mechanics allows us to go from the atomic hypothesis to theories for macroscopic behavior. We can also study the behavior of a system in detail by calculating and following the motion of each atom in the system; this is what molecular dynamics (MD) is about.

The examples below are part of the curriculum of the course FYS2160 Thermal and statistical physics. Chrome or Firefox; Safari cannot run the simulation engine.

# Lab 1 — Gas thermodynamics

**Heat capacity and compressibility of atomic Lennard-Jones** — add heat to an atomic fluid and analyse its temperature and pressure.

**Heat capacity of diatomic LJ** — compare flexible and rigid molecular bonds. The project includes the molecule definition needed by the simulation.

Open either **Lab 1** card with **Use as project**. After each completed simulation, rerun the notebook's load cell and then its plots and analysis. Keep the lab exercise sheet alongside the notebook.

# Weekly exercise, week 37

## Compressibility factor

Rearranging the ideal gas equation of state in terms of the compressibility factor, $Z=\frac{pV}{nkT}=1$, we can express deviations from the ideal gas model in terms of the virial expansion.

$Z=\frac{pV}{nkT}=1+B\rho+C\rho^2+...,$


where $\rho=n/V$ and $B$ and $C$ are the virial coefficients. This virial expansion is a macroscopic model equation of state that takes into account that the molecules have finite size and interact.
A positive second virial coefficient signifies that the final size of the molecules and repulsive interactions between them dominate a negative $B$ signifies that the attractive interactions between the molecules dominate.

##  Maxwell-Boltzmann speed distribution

In section 6.3 of Schroeder he derives the Maxwell-Boltzmann speed distribution of an ideal gas. In this short exercise you will measure the speed distribution of a Lennard-Jones liquid and solid and compare them to the Maxwell-Boltzmann speed distribution:

$  D(v)=\left(\frac{m}{2\pi kT}\right)^{3/2}4\pi v^2\exp\left(-\frac{mv^2}{2kT}\right)$.

# Seminar 6 (week 36)

**My first MD simulation** — 2D Lennard-Jones at ρ* = 0.65. Run it at T* = 0.6, 0.45 and 0.3 (`variable T` in the input file) and at constant energy. Which phases do you see? Measure the potential energy per atom and the mean-square displacement; add the pressure to the notebook's plots.

**3D diffusion MSD** — atoms diffusing in a liquid. The mean-square displacement $\mathrm{MSD}(t) = \langle |\vec r(t) - \vec r(0)|^2\rangle$ grows as $6Dt$ in three dimensions. What is the ratio of the diffusion coefficients of the two atom types, and which line in the input file causes it?

**Melting of a 2D solid** — a 2D solid heated from T* = 0.1 to 0.6: melting and evaporation. Which phases do you see, where are they in the phase diagram, and how does the slope of the mean-square displacement change?

**Heat capacity of LJ** — heat the system slowly at three densities (`variable rho`: dilute gas, liquid, solid) and read the heat capacity off the slope of energy against temperature. How does it fit with theory?

# Lecture 5 demonstrations

**A box of gas at constant pressure** and **the arrow of time** are the two runs shown in the lecture, here so that you can replay them.

# Extra

**Hot and cold in contact** — two halves of a crystal at different temperatures, released. **Pressure at three densities** — is $PV = NkT$?
