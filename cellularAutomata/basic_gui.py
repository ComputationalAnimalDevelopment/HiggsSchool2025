"""
Barebones visualization of CA simulation
"""

#################################

# System modules
import os
os.environ["QT_API"] = "PyQt6"

# Installed modules
import numpy as np
import matplotlib.cm as cm

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#PyQT6 for visualization
from PyQt6 import QtWidgets, QtCore, QtGui

#################################

class Visualization(QtWidgets.QMainWindow):

    def __init__(self, params, ca, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.params = params

        self.t        = np.arange(self.params["t_tot"])
        self.t_update = self.t[::int(self.params["freq"])]

        self.update_i = 0

        self.step = 0
        self.ca   = ca
        self.initialization = True
        
        # Initialize hexagon drawing widget
        self.xy2hex()
        x_flat = self.x.flatten()
        y_flat = self.y.flatten()
        self.centroids = np.column_stack((x_flat, y_flat))
        self.centroids*=self.params["scale"]  # Scale centroids for better visibility

        blank_data = np.zeros_like(x_flat)
        
        # Create a horizontal box layout
        hbox = QtWidgets.QHBoxLayout()
        self.widgets = []
        widget_width = params["w"] // 5

        # One for each of "Notch", "Delta", "Jagged", "Notch ICD", "VEGF Receptor"
        for i in range(5):
            widgetX = params["x0"] + i * widget_width
            widget = HexagonWidget(widgetX, self.params["y0"],
                                   widget_width, self.params["h"],
                                   self.centroids, blank_data,
                                   self.params["hs"])
            self.widgets.append(widget)
            hbox.addWidget(widget)

        # Create a central widget and set the layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Lattice Visualization")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.step_and_update)
        self.timer.start(1)  # Update every t ms
    
    
    def xy2hex(self):
        n = self.ca.g

        # Create grid coordinates for hexagonal grid
        self.x = np.zeros((n ,n))
        self.y = np.zeros((n ,n))
        for i in range(n):
            self.y[i ,:] = np.sqrt(3) * np.arange(1 , n +1 ,1 )/2.
        for i in range(n):
            if i % 2 != 0:
                self.x[: ,i] = np.arange(1, n+1 ,1)
            else:
                self.x[: ,i] = np.arange(1, n+1 ,1) + 0.5


    def update_image(self):
        # Get the current state from the CA
        N = self.ca.N[self.step]  # Notch
        D = self.ca.D[self.step]  # Delta
        J = self.ca.J[self.step]  # Jagged
        I = self.ca.I[self.step]  # Notch intracellular domain
        R = self.ca.R[self.step]  # VEGF receptor
        
        dist = [N, D, J, I, R]

        for i, (data, widget) in enumerate(zip(dist, self.widgets)):
            # Flatten the values
            flatdata = data.flatten()

            # Update the hexagon widget with new centroids and values
            widget.M = flatdata
            widget.update()

    def step_and_update(self):
        
        # Initialize
        if self.initialization:
            print("Initializing...")
            self.ca.initialize()
            
            self.initialization = False

        # Simulate normally
        else:
            self.step += 1
            self.ca.do_simstep(self.step)

            if self.step % 50 == 0:
                progress = 100 * self.step / self.params["t_tot"]
                print(f"Step: {self.step}, Progress: {progress:.1f}%")
            
        # Update visualization
        if self.step in self.t_update:
            self.update_image()
        
        # Reached final simulation step - finish
        if self.step >= self.params["t_tot"]:
            self.timer.stop()
            print("Done!")


class HexagonWidget(QtWidgets.QWidget):

    def __init__(self, x, y, w, h, centroids, M, hexsize = 2):
        super().__init__()

        self.setGeometry(x, y, w, h)
        self.setMinimumSize(w, h) 
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, 
                           QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        # Positioning of drawing within widget
        self.origin = (0, self.height() // 10)

        self.centroids = centroids
        self.M = M

        self.hexsize = hexsize

        # Colormap
        self.cmap = cm.get_cmap('viridis')
        self.norm = cm.colors.Normalize(vmin=0, vmax=5000)


    def resizeEvent(self, event):
        """Update origin when the widget is resized."""
        self.origin = (0, self.height() // 10)
        self.update()


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        for centroid, val in zip(self.centroids, self.M):
            q_color = self.get_color_from_value(val)
            
            painter.setBrush(q_color)
            painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black, 1))

            centroid_offset = [ centroid[0] + self.origin[0], 
                                centroid[1] + self.origin[1] ]
            self.draw_hexagon(painter, centroid_offset, self.hexsize)


    def get_color_from_value(self, value):
        rgba = self.cmap(self.norm(value))  # Get RGBA values from colormap

        # Convert matplotlib RGBA values (0-1) to PyQt QColor (0-255)
        return QtGui.QColor(int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255), int(rgba[3] * 255))


    def draw_hexagon(self, painter, center, size):
        points = []
        # Pointy side up: start angle at pi/6
        for i in range(6):
            angle = np.pi / 6 + 2 * np.pi * i / 6
            x = center[0] + size * np.cos(angle)
            y = center[1] + size * np.sin(angle)
            points.append(QtCore.QPointF(x, y))

        painter.drawPolygon(*points)