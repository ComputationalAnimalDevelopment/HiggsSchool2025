"""
This is the main script to run to execute the program.
"""

#################################

# System modules
import sys
from pathlib import Path

# Installed modules

#PyQT6 for visualization
from PyQt6 import QtWidgets

# Local modules
import parameters as PAR
import simulation as SIM
import basic_gui as GUI

##################################

def set_graphics_params():
    """
    Convert from the parameter names defined in the input file to a dictionary of parameters.
    """

    params = {  
              "t_ini" : PAR.T1,
              "t_tot" : PAR.T2,
              "dt"    : PAR.dt,
              "grid"  : PAR.grid,
              "freq"  : PAR.gui_update_frequency,

              "x0" : PAR.gui_X0,
              "y0" : PAR.gui_Y0,
              "w"  : PAR.gui_WINDOW_WIDTH,
              "h"  : PAR.gui_WINDOW_HEIGHT,
              "hs" : PAR.gui_hexagon_size,
              "scale" : PAR.gui_scale
             }

    return(params)

#################################

if __name__ == "__main__":

    print("Launching cellular automata simulation...")
    
    # Initialize the simulator object
    ca = SIM.Simulator(PAR.grid)

    sim_data_dir = Path('sim_data')
    sim_data_dir.mkdir(exist_ok=True)

    # Start the GUI
    gui_params = set_graphics_params()
    app = QtWidgets.QApplication(sys.argv)
    
    # Run the simulation
    window = GUI.Visualization(gui_params, ca)
    window.show()

    sys.exit(app.exec())