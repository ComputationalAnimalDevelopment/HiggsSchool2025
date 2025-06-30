"""
This is the main script to run to execute the program.
"""

#################################

# System modules
import sys

# Installed modules
import numpy as np

#PyQT6 for visualization
from PyQt6 import QtWidgets

# Local modules
import parameters as PAR
from simulation import cpm as CPM
from graphics import basic_gui as GUI

#################################

def set_simulation_params():
    """
    Convert from the parameter names defined in the input file to a dictionary of parameters.
    """

    params = {
              "A0"      : PAR.target_volume,
              "P0"      : PAR.target_surface,
              "lambda_A": PAR.lambda_volume,
              "lambda_P": PAR.lambda_surface,
              "W"       : PAR.adhesion_table,
              "T"       : PAR.kT
             }

    return(params)


def set_graphics_params():
    """
    Convert from the parameter names defined in the input file to a dictionary of parameters.
    """

    params = {  
              "scale" : PAR.gui_scale,
              "freq"  : PAR.gui_update_frequency,
              
              "colours" : PAR.gui_cell_colours,
              
              "t_tot" : PAR.total_MCS,
              "t_ini" : PAR.init_MCS,
              "t_sav" : PAR.MCS_to_save,
              "save"  : PAR.SAVE_DATA,

             }

    return(params)

#################################

if __name__ == "__main__":

    print("Launching CPM simulation...")

    # Define simulation
    sim_params = set_simulation_params()

    cpm = CPM.CPM(sim_params)
    cpm.make_grid(PAR.width, PAR.height)
    cpm.generate_cells(N_cell_dict={"E": PAR.initial_cell_number[0], 
                                    "T": PAR.initial_cell_number[1],
                                    "X": PAR.initial_cell_number[2]})

    # Initialize cells as circular patches on the sigma field
    cpm.make_init("circle", 
                  (np.sqrt(PAR.target_volume[0]) / np.pi) * 0.8, # radius of initial circle
                  (np.sqrt(PAR.target_volume[0]) / np.pi) * 0.9  # spacing between circles
                  )
    
    # Start the GUI
    gui_params = set_graphics_params()
    app = QtWidgets.QApplication(sys.argv)
    
    # Run the simulation
    window = GUI.Visualization(gui_params, cpm)
    window.show()

    sys.exit(app.exec())