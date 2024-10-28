import sys
import pandas as pd
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QPushButton, QSlider, QMessageBox
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon
import pyqtgraph as pg

from SignalClass import SignalClass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_original_signal = None
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
        self.frequency_slider.valueChanged.connect(self.change_sampling_frequency)

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
        data_x, data_y = self.open_file()
        print(len(data_x))
        if len(data_x) != 1000:
            error_message = QMessageBox()
            error_icon = QIcon("Deliverables/error_icon.png")
            error_message.setWindowIcon(error_icon)
            error_message.setWindowTitle("Data Size Error")
            error_message.setText("Please upload data of size <b>1000x2</b>.")
            error_message.exec_()

        elif data_x is not None and data_y is not None:
            original_color = (20, 200, 150)
            self.signals_uploaded_count += 1
            original_signal = SignalClass(data_x, data_y, 'original', self.first_plot_widget, original_color,
                                          self.signals_uploaded_count)
            self.original_signals_list.append(original_signal)
            self.current_original_signal = original_signal
            self.clear_plots()
            self.initialise_signals()

    def initialise_signals(self):
        self.current_original_signal.calculate_maximum_frequency()
        self.frequency_slider.setRange(0, 4 * int(self.current_original_signal.maximum_frequency))
        self.frequency_slider.setValue(int(self.current_original_signal.sampling_frequency))

        min_x = min(self.current_original_signal.data_x)
        max_x = max(self.current_original_signal.data_x)
        min_y = min(self.current_original_signal.data_y)
        max_y = max(self.current_original_signal.data_y)

        self.first_plot_widget.setLimits(xMin=min_x, xMax=max_x, yMin=min_y, yMax=max_y)
        self.second_plot_widget.setLimits(xMin=min_x, xMax=max_x, yMin=min_y, yMax=max_y)
        self.second_plot_widget.setLimits(xMin=min_x, xMax=max_x, yMin=min_y, yMax=max_y)

        print(f"max freq: {self.current_original_signal.maximum_frequency}")

        self.plot_signals()

    def plot_signals(self):
        self.current_original_signal.plot_original_signal()
        self.current_original_signal.plot_sample_points()
        self.current_original_signal.plot_reconstructed_signal(self.second_plot_widget)
        self.current_original_signal.plot_difference(self.third_plot_widget)

        print(f"sampling freq: {self.current_original_signal.sampling_frequency}")

    def clear_plots(self):
        self.first_plot_widget.clear()
        self.second_plot_widget.clear()
        self.third_plot_widget.clear()

    def change_sampling_frequency(self):
        try:
            self.current_original_signal.sampling_frequency = self.frequency_slider.value()
        except AttributeError as e:
            print(e)
        self.current_original_signal.sampling_period = 1/self.frequency_slider.value()
        self.clear_plots()
        self.plot_signals()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
