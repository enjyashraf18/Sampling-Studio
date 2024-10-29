import sys
import random
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QSlider, QLabel, \
    QLineEdit, QDialog, QComboBox
import pyqtgraph as pg
from PyQt5 import QtWidgets, uic
import pandas as pd
import os
from fileName import fileName



class composed_signal_class():
    def __init__(self, y_data, wave_type, amplitude, frequency, phase_shift, vertical_shift, signal_id):
        self.y_data = y_data
        self.wave_type = wave_type
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.vertical_shift = vertical_shift
        self.signal_id = signal_id


class SignalComposer(QMainWindow):
    composition_complete = pyqtSignal(np.ndarray,np.ndarray)
    def __init__(self, signals, plot_graph, amplitude_slider, frequency_slider,amplitude_label, frequency_label):
        super().__init__()
        self.signals = signals
        self.plot_graph = plot_graph
        self.amplitude_slider = amplitude_slider
        self.frequency_slider = frequency_slider
        self.amplitude_label = amplitude_label
        self.frequency_label = frequency_label

        self.composed_signals = []
        self.wave_type = None
        self.amplitude = None
        self.frequency = None
        self.phase_shift = None
        self.vertical_shift = None
        self.signal_id = 0
        self.cnt = 0
        self.data_x = np.linspace(0, 3, 1000)
        self.amplitude_slider_value = 1
        self.frequency_slider_value = 1
        self.composed_y_data = None
        self.save_enabled = False

        self.amplitude_slider.setValue(1)
        self.amplitude_slider.setRange(1,10 )
        self.frequency_slider.setValue(1)
        self.frequency_slider.setRange(1, 100)

        self.amplitude_slider.valueChanged.connect(self.update_amplitude_slider)
        self.frequency_slider.valueChanged.connect(self.update_frequency_slider)
        self.add_default_signal()


    def add_signal(self):
        self.save_enabled = False
        self.cnt+=1
        if self.cnt == 1:
            self.wave_type = 'sine'
        if self.cnt == 2:
            self.wave_type = 'cosine'
        if self.cnt == 3:
            self.wave_type = 'sine'

        self.amplitude = int(self.amplitude_slider_value)
        self.frequency = int(self.frequency_slider_value)
        self.phase_shift = 0
        self.vertical_shift = 0
        self.signal_id +=1
        
        if self.wave_type == 'sine':
            y_values = (self.amplitude * np.sin(self.frequency * self.data_x + self.phase_shift) + self.vertical_shift)
        elif self.wave_type == 'cosine':
            y_values = (self.amplitude * np.cos(self.frequency * self.data_x + self.phase_shift) + self.vertical_shift)
        created_signal = composed_signal_class(y_values, self.wave_type, self.amplitude, self.frequency, self.phase_shift, self.vertical_shift, self.signal_id)
        self.composed_signals.append(created_signal)
        self.signals.addItem(f'signal {self.signal_id}' )
        self.compose_and_plot()

    def add_default_signal(self):
        self.wave_type = 'sine'
        self.amplitude = 2
        self.frequency = 8
        self.phase_shift = 0
        self.vertical_shift = 0
        self.signal_id +=1
        y_values = (self.amplitude * np.sin(self.frequency * self.data_x + self.phase_shift) + self.vertical_shift)

        created_signal = composed_signal_class(y_values, self.wave_type, self.amplitude, self.frequency, self.phase_shift, self.vertical_shift, self.signal_id)
        self.composed_signals.append(created_signal)
        self.signals.addItem(f'Component {self.signal_id}')
        self.compose_and_plot()


    def update_amplitude_slider(self):
        try:
            print("ay 7agaaa")
            self.amplitude_slider_value = self.amplitude_slider.value()
            print(self.amplitude_slider_value)
        except AttributeError as e:
            print("ay 7agaaa 2")
            print(e)
        self.amplitude_label.setText(str(self.amplitude_slider.value()))

    def update_frequency_slider(self):
        try:
            self.frequency_slider_value = self.frequency_slider.value()
        except AttributeError as e:
            print(e)
        self.frequency_label.setText(str(self.frequency_slider.value()))



    def delete_signal(self):
        signal_id_to_delete = self.signals.currentIndex() + 1
        if signal_id_to_delete is not None:
            self.composed_signals = [signal for signal in self.composed_signals if
                                     signal.signal_id != signal_id_to_delete]
            self.signals.removeItem(signal_id_to_delete - 1)
            self.compose_and_plot()

    def compose_and_plot(self):
        print("compose and delete")
        self.plot_graph.clear()
        self.composed_y_data = np.zeros_like(self.data_x)
        for signal in self.composed_signals:
            self.composed_y_data += signal.y_data
        self.plot_graph.plot(self.data_x, self.composed_y_data, pen='r', name='Composed Signal')

    def save_data_to_csv(self, file_name):
        # convert it to csv file
        save_directory = 'composed_signals/'
        df = pd.DataFrame({
            'X': self.data_x,
            'Y': self.composed_y_data
        })
        file_name = file_name
        file_path = os.path.join(save_directory, file_name)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
        


    def enter_file_name(self):
        print("enter file name")
        dialog = fileName()
        dialog.center_on_screen()
        if dialog.exec_():
            file_name = dialog.file_name
            self.save_data_to_csv(file_name)
            return self.data_x, self.composed_y_data






