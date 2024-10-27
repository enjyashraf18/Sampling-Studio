import sys
import pandas as pd
import numpy as np
import scipy.signal
# from MainWindowTemp import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg

from pyqtgraph import ScatterPlotItem
from scipy.interpolate import interp1d
from scipy import special  # For sinc function


def whittaker_shannon_interpolation(x_points, sampled_x, sampled_y, sampling_period):
    sinc_matrix = np.tile(x_points, (len(sampled_x), 1)) - np.tile(sampled_x[:, None], (1, len(x_points)))
    reconstructed_y = np.dot(sampled_y, np.sinc(sinc_matrix / sampling_period))
    return reconstructed_y


class SignalClass:
    def __init__(self, data_x, data_y, signal_type, plot_widget, color, signal_id):
        self.data_x = data_x
        self.data_y = data_y
        self.type = signal_type  # original, reconstructed, difference
        self.plot_widget = plot_widget
        self.color = color
        self.signal_id = signal_id
        self.maximum_frequency = None
        self.sampling_frequency = 360
        self.sampling_period = 1 / self.sampling_frequency
        self.x_sampled = None
        self.y_sampled = None
        self.y_reconstructed = None

        # self.signal_number = signal_number
        # self.amplitude_data = self.y_data
        # self.amplitude = amplitude
        # self.line = self.plot_widget.plot(data_x, self.amplitude_data, pen=pg.mkPen(color=self.color, width=2),
        # name=f"Signal{str(self.signal_number)}")

    def calculate_maximum_frequency(self):
        self.maximum_frequency = None

    def plot_original_signal(self):
        self.plot_widget.plot(self.data_x, self.data_y, pen=self.color)

    def plot_sample_points(self):
        sample_start = np.min(self.data_x)
        sample_end = np.max(self.data_x)
        self.x_sampled = np.arange(sample_start, sample_end, self.sampling_period)
        self.y_sampled = np.interp(self.x_sampled, self.data_x, self.data_y)
        # for x, y in zip(self.data_x, self.data_y):
        #     if x in x_sampled:
        #         y_sampled.append(y)
        self.plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=5, symbolBrush='w')
        print(self.y_sampled)

    def plot_reconstructed_signal(self, second_plot_widget):
        self.y_reconstructed = whittaker_shannon_interpolation(self.data_x, self.x_sampled, self.y_sampled,
                                                               self.sampling_period)
        second_plot_widget.plot(self.data_x, self.y_reconstructed, pen=(50, 100, 240))

        # do we need to create an object for reconstructed signal?

        # reconstructed_color = (200, 0, 50)
        # reconstructed_signal = SignalClass(self.data_x, y_reconstructed, 'reconstructed', second_plot_widget,
        #                                    reconstructed_color, 0)
        # reconstructed_signal.plot_widget(reconstructed_signal.data_x,
        #                                  reconstructed_signal.data_y, pen=reconstructed_color)

    def plot_difference(self, third_plot_widget):
        difference_y = self.data_y - self.y_reconstructed
        third_plot_widget.plot(self.data_x, difference_y, pen=(200, 50, 50))

    # def update_amplitude(self, amplitude):
    #     self.amplitude_data = [amplitude + val for val in self.amplitude_data]
    #     self.amplitude = int(max(self.amplitude_data))
    #     self.line.setData(self.x_data, self.amplitude_data)

# class reconstructed_signal_class:
#     def __init__(self, data_x, data_y, signal_type):
#         self.x = data_x
#         self.y = data_y
#         self.type = signal_type  # original, reconstructed, difference
#         # self.plot_widget = plot_widget
#         self.color = None


# def plot_original(self):
#
#     # Sampling parameters
#     sampling_frequency = 250
#     sampling_period = 1 / sampling_frequency
#     self.x_sampled = np.arange(np.min(signal_x), np.max(signal_x), sampling_period)
#
#     # Sampled signal using interpolation
#     self.y_sampled = np.interp(self.x_sampled, signal_x, self.signal_y)
#
#     # Plot the sampled points on the first plot widget
#     self.first_plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=5, symbolBrush='w')
#
#     # Plot the reconstructed sampled signal on the second plot widget
#     # self.second_plot_widget.plot(self.x_sampled, self.y_sampled, pen='g')
#
#     # Reconstruct signal on original `signal_x` using Whittaker-Shannon interpolation
#     # Calculate and plot the difference on the third plot widget
#     difference = self.signal_y - self.y_reconstructed
#
#     self.third_plot_widget.plot(signal_x, difference, pen='r')
#
# def reconstruct_signal(self, data_x, x_sampled, y_sampled, sampling_frequency):
#     reconstructed_signal = Signal(x_sampled, y_sampled, 'reconstructed')
#     recovered_y, recovered_x = scipy.signal.resample(self.x_sampled)
#     self.y_reconstructed = whittaker_shannon_interpolation(data_x, self.x_sampled, self.y_sampled)
#     main_window.second_plot_widget.plot(data_x, self.y_reconstructed, pen='r')
#
# def plot_difference(self):
#     pass


# def reconstruct_signal(self, signal, time_sampled, sampled_signal):
#     time_domain = np.linspace(0, signal.x[-1], len(signal.x))
#     # Creating a 2D matrix with len(time_sampled) rows and len(time_domain) coloumns
#     resizing = np.resize(time_domain, (len(time_sampled), len(time_domain)))
#     Fs = 1 / (time_sampled[1] - time_sampled[0])
#     # Subtract the sample time within the time domain from the 2 columns
#     pre_interpolation = (resizing.T - time_sampled) * Fs
#     '''Get the sinc value for each value in the resizing matrix so within 0 the value will be 1 and for large
#     values it will be zero then multiply these values with its real amplitudes'''
#     interpolation = sampled_signal * np.sinc(pre_interpolation)
#
#     # x(t)=∑ n=−∞ ---> ∞ [x[n]⋅sinc(fs * (t-nTs))
#     # t ---> time domain
#     # X[n] ---> samples
#     # Ts ---> 1/fs
#
#     # Get the sum of the columns within one column only with the required data
#     samples_of_amplitude_at_time_domain = np.sum(interpolation, axis=1)
#
#     return time_domain, samples_of_amplitude_at_time_domain
