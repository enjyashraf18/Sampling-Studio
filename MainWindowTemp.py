import sys
import pandas as pd
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QPushButton, QSlider
from PyQt5.QtCore import QRect, Qt
import pyqtgraph as pg

from SignalClass import SignalClass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_signals_list = []
        self.signals_uploaded_count = 0

        self.first_plot_widget = pg.PlotWidget()
        self.second_plot_widget = pg.PlotWidget()
        self.third_plot_widget = pg.PlotWidget()
        self.fourth_plot_widget = pg.PlotWidget()
        self.frequency_slider = QSlider()

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
        # upload_amplitude_button.clicked.connect(change_amplitude)

        self.frequency_slider.setGeometry(QRect(190, 100, 160, 16))
        self.frequency_slider.setOrientation(Qt.Horizontal)
        # self.frequency_slider.valueChanged.connect()

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(upload_button)
        layout.addWidget(self.first_plot_widget)
        layout.addWidget(self.second_plot_widget)
        layout.addWidget(self.third_plot_widget)
        layout.addWidget(self.fourth_plot_widget)
        layout.addWidget(self.frequency_slider)

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
                print(f"Error, couldn't upload: {e}")
                return None, None
        else:
            return None, None

    def upload_signal(self):
        print("uploading 1st and 2nd signals")
        data_x, data_y = self.open_file()
        if data_x is not None and data_y is not None:
            original_color = (20, 200, 150)
            self.signals_uploaded_count += 1
            original_signal = SignalClass(data_x, data_y, 'original', self.first_plot_widget, original_color,
                                          self.signals_uploaded_count)
            self.original_signals_list.append(original_signal)
            self.plot_signals(original_signal)

    def plot_signals(self, original_signal):
        original_signal.plot_original_signal()
        original_signal.plot_sample_points()
        original_signal.plot_reconstructed_signal(self.second_plot_widget)
        original_signal.plot_difference(self.third_plot_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
