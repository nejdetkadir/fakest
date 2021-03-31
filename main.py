import sys
from PyQt5 import QtWidgets
from ui import UI

app = QtWidgets.QApplication(sys.argv)
ui = UI(app)
sys.exit(app.exec_())