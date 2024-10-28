import sys
import random
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QSlider, QLabel, QLineEdit
import pyqtgraph as pg


class composed_signal_class:
    def __init__(self, y_data, wave_type, amplitude, frequency, phase_shift, vertical_shift, signal_id):
        self.y_data = y_data
        self.wave_type = wave_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.vertical_shift = vertical_shift
        self.signal_id = signal_id


class SignalComposer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.composed_signals = []
        self.wave_type = None
        self.amplitude = None
        self.frequency = None
        self.phase_shift = None
        self.vertical_shift = None
        self.signal_id = 0
        self.cnt = 0
        self.data_x = np.linspace(0, 3, 1000)

        self.setWindowTitle("Signal Composer")
        self.setGeometry(100, 100, 1200, 800)
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        self.freq_input = QLineEdit(self)
        self.freq_input.setPlaceholderText("Frequency (Hz)")
        self.main_layout.addWidget(self.freq_input)

        self.magnitude_input = QLineEdit(self)
        self.magnitude_input.setPlaceholderText("Magnitude")
        self.main_layout.addWidget(self.magnitude_input)

        add_signal_button = QPushButton("Add signal", self)
        add_signal_button.setStyleSheet("font-size: 20px;")
        add_signal_button.clicked.connect(self.add_signal)
        self.main_layout.addWidget(add_signal_button)

        delete_signal_button = QPushButton("delete signal", self)
        delete_signal_button.setStyleSheet("font-size: 20px;")
        delete_signal_button.clicked.connect(self.delete_signal)
        self.main_layout.addWidget(delete_signal_button)

        plot_button = QPushButton("compose and plot signals", self)
        plot_button.setStyleSheet("font-size: 20px;")
        plot_button.clicked.connect(self.compose_and_plot)
        self.main_layout.addWidget(plot_button)

        self.signal_id_input = QLineEdit(self)
        self.signal_id_input.setPlaceholderText("Signal ID to delete")
        self.main_layout.addWidget(self.signal_id_input)

        self.plot_graph = pg.PlotWidget()
        self.main_layout.addWidget(self.plot_graph)


    def add_signal(self):
        self.cnt+=1
        if self.cnt == 1:
            self.wave_type = 'sine'
        if self.cnt == 2:
            self.wave_type = 'cosine'
        if self.cnt == 3:
            self.wave_type = 'sine'

        self.amplitude = float(self.magnitude_input.text())
        self.frequency = float(self.freq_input.text())
        self.phase_shift = 0
        self.vertical_shift = 0



        self.signal_id +=1
        if self.wave_type == 'sine':
            y_values = (self.amplitude * np.sin(self.frequency * self.data_x + self.phase_shift) + self.vertical_shift)
        elif self.wave_type == 'cosine':
            y_values = (self.amplitude * np.cos(self.frequency * self.data_x + self.phase_shift) + self.vertical_shift)
        created_signal = composed_signal_class(y_values, self.wave_type, self.amplitude, self.frequency, self.phase_shift, self.vertical_shift, self.signal_id)
        self.composed_signals.append(created_signal)
        self.freq_input.clear()
        self.magnitude_input.clear()



    def delete_signal(self):
        signal_id_to_delete = int(self.signal_id_input.text()) if self.signal_id_input.text() else None
        if signal_id_to_delete is not None:
            self.composed_signals = [signal for signal in self.composed_signals if
                                     signal.signal_id != signal_id_to_delete]
            self.signal_id_input.clear()
            self.compose_and_plot()

    def compose_and_plot(self):
        self.plot_graph.clear()
        composed_y_data = np.zeros_like(self.data_x)
        for signal in self.composed_signals:
            composed_y_data += signal.y_data
        self.plot_graph.plot(self.data_x, composed_y_data, pen='r', name='Composed Signal')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalComposer()
    window.show()
    sys.exit(app.exec_())