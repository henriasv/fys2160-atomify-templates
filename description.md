# Introduction

Statistical mechanics allows us to go from the atomic hypothesis to theories for macroscopic behavior. We can also study the behavior of a system in detail by calculating and following the motion of each atom in the system, this is what molecular dynamics (MD) is about.

The following examples, exercises and projects using MD are part of the curriculum of the course Fys2160 Thermal and statistical physics.

# First simulation using Atomify Lammps

**My first MD simulation**

This will familiarize you with running and analyzing simulations in Atomify.

**Melting of a 2D solid**

Heating a 2D solid from low temperature to high temperature we observe the melting and evaporation process

**Heat capacity of LJ**

Once again we heat the system, now to measure the heat capacity of LJ gas, liquid and solid.

# Diffusion simulations

**3D diffusion MSD**

In these simulations, we simulate atoms diffusing in a liquid and measure the diffusion coefficient using methods like mean square displacement and velocity auto correlation.

The mean square displacement in the x-direction is defined as 

$MSD = \langle (\vec x(t) - \vec x_0)^2\rangle  = \frac{1}{N}\sum_{i=1}^{N} |\vec x^{(i)}(t) - \vec x^{(i)}_0|^2$

and relates to the diffusion coefficient $D$ as

$D = \frac{\langle (\vec x(t) - \vec x_0)^2\rangle}{2t}$

where $t$ is the time.