import sys
from PyQt4 import QtGui, QtCore

# application variables
width, height = 500, 500 # main window width, height

app = QtGui.QApplication(sys.argv) # declare app

# User screen dimensions
screen_resolution = app.desktop().screenGeometry()
s_width, s_height = screen_resolution.width(), screen_resolution.height()

window = QtGui.QWidget() # declare main window

# Start application in center of the users screen:
window.setGeometry((s_width/2)-(width/2), (s_height/2)-(height/2), width, height)

window.setWindowTitle("Test Application") # main window title

#window.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

window.setFixedSize(window.size()) #set fixed window size
window.show() # display main window

sys.exit(app.exec_()) # keep application open
