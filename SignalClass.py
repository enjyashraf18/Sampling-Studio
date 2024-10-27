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
    reconstructed = np.dot(sampled_y, np.sinc(sinc_matrix / sampling_period))
    return reconstructed


class SignalClass:
    def __init__(self, data_x, data_y, signal_type, amplitude, plot_widget, color, signal_number, signal_id):
        self.x_data = data_x
        self.y_data = data_y
        self.type = signal_type  # original, reconstructed, difference
        # self.amplitude_data = self.y_data
        # self.amplitude = amplitude
        self.plot_widget = plot_widget
        self.color = color
        # self.signal_number = signal_number
        self.signal_id = signal_id
        # self.line = self.plot_widget.plot(data_x, self.amplitude_data, pen=pg.mkPen(color=self.color, width=2), name=f"Signal{str(self.signal_number)}")


    def plot_original_signal(self, data_x, data_y, amplitude, first_plot, color, signal_id):
        # signal = SignalClass(data_x, data_y, 'original', amplitude, first_plot, color, len(original_signals_list) + 1, signal_id)
        # chosen_signal = signal
        # original_signals_list.append(signal)
        pass


    def plot_reconstructed_signal(self, data_x, data_y, sampling_period, second_plot):
        x_sampled = np.arange(np.min(data_x), np.max(data_x), sampling_period)
        y_sampled = np.interp(x_sampled, data_x, data_y)
        # reconstructed_signal = reconstructed_signal_class(x_sampled, y_sampled, 'reconstructed')
        # recovered_y, recovered_x = scipy.signal.resample(x_sampled)
        y_reconstructed = whittaker_shannon_interpolation(data_x, x_sampled, y_sampled, sampling_period)
        second_plot.plot(data_x, y_reconstructed, pen='r')

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
