# Overview

This repository consists of subfolders containing self-contained simulations with a basic real-time visualization.
To run the simulation code you will need Python 3.10 or above installed on your system.

# Tutorial

## Cellular Automata
- Consult the readme file in the appropriate subfolder to learn how to use the code.
- Study how the Hill functions behave with change of parameters using the script ```visualize_Hill_function.py```.
- Try the simulation with default parameters and see what happens.
- Explore the code: Where are the "internal rules" defined? Where is the neighbourhood defined?
- Try simulating with different initial VEGF concentrations and compare the visual output.

## Cellular Potts
- Consult the readme file in the appropriate subfolder to learn how to use the code.
- Try the simulation with default parameters and see what happens.
- Explore the code: Where are the "internal rules" defined? Where is the neighbourhood defined?
- Try some simple cell sorting simulations. Observe how changing adhesion affinities leads to different cell configurations. For simplicity, change the parameters such that no third cell type is generated. Then adjust the values of the adhesion table for the two remaining cell types:
  - Set equal adhesion affinities for all cell-cell interactions. Leave affinity to the medium at a low value.
  - Set the adhesion affinity of cell type 1 to itself to a larger value.
  - Set the affinities such that cell-medium interactions are more favourable than any cell-cell interactions.
- Explore how other parameters such as volume and surface constraints affect the cell sorting simulations.
