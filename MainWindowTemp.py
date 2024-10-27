import sys
import pandas as pd
import random
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

        self.signal_id = 0


    def init_ui(self):
        self.setWindowTitle('Sampling Studio')
        self.setGeometry(0, 100, 2500, 1300)

        upload_button = QPushButton("Upload")
        upload_button.setGeometry(0, 0, 100, 100)
        upload_button.clicked.connect(self.upload_signal)

        upload_amplitude_button = QPushButton("Change Amplitude")
        upload_amplitude_button.setGeometry(0, 100, 50, 50)
        upload_amplitude_button.clicked.connect(change_amplitude)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(upload_button)
        layout.addWidget(self.first_plot_widget)
        layout.addWidget(self.second_plot_widget)
        layout.addWidget(self.third_plot_widget)
        layout.addWidget(self.fourth_plot_widget)

    # def upload_csv(self):
    #     options = QFileDialog.Options()
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
    #     if file_name:
    #         data = pd.read_csv(file_name)
    #         data_x = data.iloc[:, 0].values
    #         data_y = data.iloc[:, 1].values
    #         plot_original_signal(data_x, data_y, self.first_plot_widget)
    #         plot_reconstructed_signal(data_x, data_y, 1 / 500, self.second_plot_widget)

    def upload_signal(self):
        print("uploading 1st and 2nd signals")
        data_x, data_y = self.open_file()
        if data_x is not None and data_y is not None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            amplitude = int(max(data_y))
            self.signal_id += 1
            plot_original_signal(data_x, data_y, amplitude, self.first_plot_widget, color, self.signal_id)
            plot_reconstructed_signal(data_x, data_y, 1 / 500, self.second_plot_widget)


    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        path = filename[0]
        if path:
            try:
                data = pd.read_csv(path)
                x = data.iloc[:, 0].values
                y = data.iloc[:, 1].values
                return x, y
            except Exception as e:
                print(f"error, couldnt upload: {e}")
                return None, None
        else:
            return None, None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())






