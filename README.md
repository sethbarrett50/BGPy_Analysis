# BGPy_Analysis

## Overview
This repository contains the code associated with our work-in-progress paper titled "Ain't How You Deploy: An Analytical Analysis of BGP Security Policies Performance Against Various Attack Scenarios with Differing Deployment Strategies".

### Authors
- Seth Barrett - [sebarrett@augusta.edu](mailto:sebarrett@augusta.edu)
- Calvin Idom - [cli025@email.latech.edu](mailto:cli025@email.latech.edu)
- German Zavala Villafuerte - [gzava010@jaguar.tamu.edu](mailto:gzava010@jaguar.tamu.edu)
- Andrew Byers - [adbyers1@asu.edu](mailto:adbyers1@asu.edu)
- Berk Gulmezoglu - [bgulmez@iastate.edu](mailto:bgulmez@iastate.edu)

## Acknowledgments
We would like to express our gratitude to the authors of BGPy for their excellent simulation framework and their assistance. You can find more about BGPy in the following publication:

- Justin Furuness, Cameron Morris, Reynaldo Morillo, Amir Herzberg, Bing Wang, "BGPy: The BGP Python Security Simulator", Proceedings of the 16th Cyber Security Experimentation and Test Workshop, 2023. [DOI: 10.1145/3607505.3607509](https://doi.org/10.1145/3607505.3607509)

## Project Layout
- `simRunner`: Contains the Python code used for running simulations with BGPy.
- `simOutput`: Stores all output files from our simulations.
- `dataAnalysis`: Includes the Julia code for data concatenation and Jupyter notebooks for further exploratory data analysis.

## Usage
This project is designed to run on an M1 MacBook, with specific adaptations made to the BGPy package on commit `de44b54`. For setup and usage instructions, refer to the [BGPy Tutorial](https://github.com/jfuruness/bgpy_pkg/wiki/Tutorial). Ensure Julia is installed on your system, as our data analysis scripts require it. These scripts will automatically install necessary Julia packages.

## Open Source Justification
We are open sourcing our code to be transparent and to benefit from community insights, especially to identify and correct any potential errors in our simulation or analysis processes.

## License
This project is released under the [Unlicense](https://unlicense.org/).
