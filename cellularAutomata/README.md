# Cellular Automata

This repository contains a cellular automata implementation based on source code provided with the publication of [Kang et al., eLife 2024]( https://doi.org/10.7554/eLife.89262.3). 
The code was refactored to be more modular and was extended with a basic graphical user interface for real-time visualization using PyQt6.


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
- The file "parameters.py" is used to define parameters used for the simulation and for the visualization.
- The file "simulation.py" contains the core simulation engine. It calls on "sim_functions.py" for the numerical computation.
- The file "basic_gui.py" implements a simple visualization.
