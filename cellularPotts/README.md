# Cellular Potts Model

The [Cellular Potts Model (CPM)](https://en.wikipedia.org/wiki/Cellular_Potts_model), also known as the Glazier-Graner-Hogeweg (GGH) model, is a lattice cell based modelling framework widely used in computational biology to study processes such as cell sorting, tissue growth, and morphogenesis.

The model simulates the dynamics of cells on a grid, where each cell is represented by a set of lattice sites. The evolution of the system is driven by an energy function, traditionally termed "Hamiltonian". Cells update their configurations using a modified Metropolis-Hastings algorithm to minimize their energy.

This repository contains an implementation of the CPM that was forked from source code provided with the publication of [Bao et al., Nature Cell Biology 2022](https://doi.org/10.1038/s41556-022-00984-y). 
The code was refactored to be more modular and was extended with a basic graphical user interface for real-time visualization using PyQt6.
The GitHub repository with the original code can be found at: https://github.com/jakesorel/CPM_ETX_2022


# How to Use

To run the simulation, you will need Python 3.10 or above installed on your system. It is recommended to use a virtual environment to manage Python dependencies (see next section for instructions on how to do this).

Once you have set up the virtual environment and activated it, you can run simulations from the project directory by running the following command in the terminal or command prompt:
```bash
   python main.py
```
(or, on Windows: ```python .\main.py```)


## Setting Up a Virtual Environment

Set up a virtual environment by following these steps:

1. **Create a Virtual Environment:**

   Open your terminal or command prompt and navigate to the project directory. Then, create a virtual environment by running:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**

    - On Windows, activate the virtual environment by running:
    ```.\venv\Scripts\activate```

    - On Linux or macOS, activate the virtual environment by running:
    ```source venv/bin/activate```

3. **Install dependencies**

    Once the virtual environment is activated, you can install the necessary dependencies using pip and the provided requirements.txt file:

    ```pip install -r requirements.txt```


To exit the virtual environment just run:

    deactivate


## Code Structure

The code is organized as follows:

- The file "main.py" is the entry-point script that should be executed to run the simulation.
- The file "parameters.py" is used to define parameters used for the CPM simulation and for the visualization.
- The subfolder "CPM" contains the core simulation code forked from [jakesorel/CPM_ETX_2022](https://github.com/jakesorel/CPM_ETX_2022).
- The subfolder "GUI" contains a simple PyQt6-based visualization.
