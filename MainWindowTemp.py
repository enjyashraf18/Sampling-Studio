import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QPushButton
from PyQt5.QtGui import QColor
import pyqtgraph as pg
from main import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.first_plot_widget = pg.PlotWidget()
        self.second_plot_widget = pg.PlotWidget()
        self.third_plot_widget = pg.PlotWidget()
        self.fourth_plot_widget = pg.PlotWidget()

        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle('Sampling Studio')
        self.setGeometry(0, 100, 2500, 1300)

        upload_button = QPushButton("Upload")
        upload_button.setGeometry(0, 0, 100, 100)
        upload_button.clicked.connect(self.upload_csv)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(upload_button)
        layout.addWidget(self.first_plot_widget)
        layout.addWidget(self.second_plot_widget)
        layout.addWidget(self.third_plot_widget)
        layout.addWidget(self.fourth_plot_widget)

    def upload_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        if file_name:
            dataframe = pd.read_csv(file_name)
            data_x = dataframe.iloc[:, 0].values
            data_y = dataframe.iloc[:, 1].values
            plot_original_signal(data_x, data_y, self.first_plot_widget)
            plot_reconstructed_signal(data_x, data_y, 1 / 500, self.second_plot_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())






