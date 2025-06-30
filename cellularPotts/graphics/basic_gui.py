"""
Barebones visualization of CPM simulation
"""

#################################

# System modules
from pathlib import Path
import datetime

# Installed modules
import numpy as np

#PyQT6 and fastplotlib for visualization
from PyQt6 import QtWidgets, QtCore, QtGui

#################################

class Visualization(QtWidgets.QMainWindow):

    def __init__(self, params, cpm, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.label = QtWidgets.QLabel()
        self.setCentralWidget(self.label)
        self.setWindowTitle("CPM Visualization")

        self.params = params

        self.t        = np.arange(self.params["t_tot"])
        self.t_update = self.t[::int(self.params["freq"])]

        self.update_i = 0

        self.MCS = 0
        self.cpm = cpm
        self.initialization = True
        self.set_colour_table()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.step_and_update)
        self.timer.start(1)  # Update every t ms
    

    def set_colour_table(self):
        # Create colourmap

        c_ids = self.cpm.cell_ids # unique non-zero sigma values
        ctype = self.cpm.c_types  # list of cell types, maps 1-to-1 to c_ids
        
        # Create a mapping from cell ID to colour index
        # id_to_colour_index is a 1D array where the index represents a cell ID, 
        # and the value at that index represents the corresponding colour index
        self.id_to_colour_index = np.zeros(np.max(c_ids) + 1, dtype=np.uint8)
        self.id_to_colour_index[1:] = np.asarray(ctype) # First element (0) is background index
        
        # colour table for QImage
        self.colourtable = []
        for _, v in self.params["colours"].items():
            self.colourtable += [QtGui.qRgb(*v)]
        

    def update_image(self):
        
        sigma = self.cpm.sigma_field  # cpm.sigma_field is a 2D array

        # Scale up the array for visualization
        res = self.params["scale"]
        I_scale = np.repeat(np.repeat(sigma, res, axis=0), res, axis=1)

        # Set the cell boundaries to a special value to colour them differently
        boundaries = self.cpm.get_perimeter_elements(I_scale)

        # Map scaled sigma field to colour indices
        sigma_colour_indices = self.id_to_colour_index[I_scale]
        sigma_colour_indices[boundaries] = len(self.colourtable)-1 # last index of colourtable

        # Convert to 8-bit for QImage
        sigma8 = sigma_colour_indices.astype(np.uint8)

        h, w = sigma8.shape
        img = QtGui.QImage(sigma8.data, w, h, w, QtGui.QImage.Format.Format_Indexed8)
        img.setColorTable(self.colourtable)
        pix = QtGui.QPixmap.fromImage(img)
        self.label.setPixmap(pix)


    def step_and_update(self):

        self.MCS += 1
        
        # Initialize with a J-matrix that favors cell separation
        if self.initialization:
            self.cpm.simulate_with_gui(self.params["t_tot"], self.params["t_sav"], self.MCS, 
                                       initialize=True, J0=-8, n_initialise_steps = self.params["t_ini"])
            self.initialization = False

        # Simulate normally
        else:
            self.cpm.simulate_with_gui(self.params["t_tot"], self.params["t_sav"], self.MCS, initialize=False)
        
        # Update visualization
        if self.MCS in self.t_update:
            self.update_image()
            self.update_i += 1
        
        # Reached final simulation step - finish
        if self.MCS >= self.params["t_tot"]:
            self.timer.stop()
            print("Progress: 100.0 %")
            
            # Save the simulation data
            if self.params["save"]:
                basepath = Path(__file__).parent
                out_dir  = basepath / "output"
                out_dir.mkdir(exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                self.cpm.save_simulation(out_dir, "CPM_sim__" + timestamp)
            
            print("Done!")