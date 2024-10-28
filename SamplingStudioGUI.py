from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("SamplingStudio.ui", self)

        # self.binButton= self.findChild(QButton, bin2)

app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
