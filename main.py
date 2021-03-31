"""
f = Fakest()
f.login("191203066", "UZYDAR")
f.whichLesson("https://lms.bandirma.edu.tr/Activity/Index/CC6E22810A041943820E3D2F675C3B4F")
f.whichWeek()
time.sleep(50 * 10)
f.quit()
"""
import sys
from PyQt5 import QtWidgets
from ui import UI

app = QtWidgets.QApplication(sys.argv)

ui = UI(app)

sys.exit(app.exec_())