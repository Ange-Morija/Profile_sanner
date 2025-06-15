import sys
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph import opengl as gl
import numpy as np

class MyMainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # Define some window Name
        self.setWindowTitle("3D points viewer")
        
        # Set size of the window in pixels (width, height)
        self.resize(1440 ,900)
        
        # Create an empty OpenGL window
        self.win = gl.GLViewWidget()
        
        # Set background color RGB and Alpha
        self.win.setBackgroundColor((250, 250, 250, 0))
        
        # Set the central widget as the empty OpenGL window
        self.setCentralWidget(self.win)
        

    def display_xyz(self, coordinates_path):
        
        # Load 3D coordinates as a numpy array
        xyz = np.loadtxt(coordinates_path)
        
        # Create Scatter plot item with the xyz positions and some attributes
        pc_color = (1,0,0,1) #RGB and Alpha value
        pc_size = 3 # Points size value
        self.coordinates = gl.GLScatterPlotItem(size=pc_size, pos=xyz, color=pc_color) # create 3D scatter plot
        self.coordinates.setGLOptions("opaque") # Apply rendering method
        
        # Set some camera options
        camera_x = np.mean(xyz[:,0]) # mean of the x values
        camera_y = np.mean(xyz[:,1]) # mean of the y values
        camera_z = np.mean(xyz[:,2]) # mean of the z values
    
        self.win.opts["center"] = pg.Qt.QtGui.QVector3D(camera_x,camera_y,camera_z) # camera center
        self.win.opts["distance"] = 12 # distance of camera from center
        self.win.opts['elevation'] = 50 # camera's angle of elevation in degrees
        self.win.opts['azimuth'] = 50 # camera's azimuthal angle in degrees 	
        
        # Add 3D scatter plot to the main window
        self.win.addItem(self.coordinates)
    

if __name__ == "__main__":
    
    app = QApplication([])
    foo = MyMainWindow()
    foo.show()
    foo.display_xyz("python_helper/Cloud_06.txt") # Call the display_point_cloud function
    
    sys.exit(app.exec_())