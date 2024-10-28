import sys
import pandas as pd
import numpy as np
import scipy.signal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph import ScatterPlotItem
from scipy.interpolate import interp1d
from scipy import special  # For sinc function
from scipy.interpolate import CubicSpline

def cubic_spline_interpolation(x_points,sampled_x,sampled_y):
    cs_func = CubicSpline(sampled_x,sampled_y)
    reconstructed_y= cs_func(x_points)
    return reconstructed_y


# Shannon (sinc) interpolation function
def whittaker_shannon_interpolation(x_points, sampled_x, sampled_y, sampling_period):
    sinc_matrix = np.tile(x_points, (len(sampled_x), 1)) - np.tile(sampled_x[:, None], (1, len(x_points)))
    reconstructed_y = np.dot(sampled_y, np.sinc(sinc_matrix / sampling_period))
    return reconstructed_y


# Lanczos interpolation function (sinc modified filter)
def lanczos_interpolation(x_points, sampled_x, sampled_y, a=3):
    def lanczos_kernel(x, a):
        if x == 0:
            return 1
        elif -a < x < a:
            return a * np.sin(np.pi * x) * np.sin(np.pi * x / a) / (np.pi ** 2 * x ** 2)
        else:
            return 0

    # intilzie to fill
    reconstructed_y = np.zeros_like(x_points)

    for i, t in enumerate(x_points):
        # Sum contributions from all sampled points, weighted by the Lanczos kernel
        for j, t_j in enumerate(sampled_x):
            x = (t - t_j) / (sampled_x[1] - sampled_x[0])  # Relative distance
            reconstructed_y[i] += sampled_y[j] * lanczos_kernel(x, a)

    return reconstructed_y


# Signal class definition
class SignalClass:
    def __init__(self, data_x, data_y, signal_type, plot_widget, color, signal_id):
        self.data_x = data_x
        self.data_y = data_y
        self.type = signal_type  # original, reconstructed, difference
        self.plot_widget = plot_widget
        self.color = color
        self.signal_id = signal_id
        self.maximum_frequency = None
        self.sampling_frequency = 100
        self.sampling_period = 1 / self.sampling_frequency
        self.x_sampled = None
        self.y_sampled = None
        self.y_reconstructed = None

    def calculate_maximum_frequency(self):
        self.maximum_frequency = None

    def plot_original_signal(self):
        self.plot_widget.plot(self.data_x, self.data_y, pen=self.color)

    def plot_sample_points(self):
        sample_start = np.min(self.data_x)
        sample_end = np.max(self.data_x)
        self.x_sampled = np.arange(sample_start, sample_end, self.sampling_period)
        self.y_sampled = np.interp(self.x_sampled, self.data_x, self.data_y)
        self.plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=5, symbolBrush='w')
        print(self.y_sampled)

    def plot_reconstructed_signal(self, second_plot_widget, method='cubic_spline'):
        if method == 'shannon':
            reconstructed_time = np.linspace(self.start_time, self.end_time, 1000)
            self.y_reconstructed = whittaker_shannon_interpolation(self.x_sampled, self.y_sampled,
                                                                   reconstructed_time)
        elif method == 'lanczos':
            self.y_reconstructed = lanczos_interpolation(self.data_x, self.x_sampled, self.y_sampled, a=3)
        elif method == 'cubic_spline':
            self.y_reconstructed = cubic_spline_interpolation(self.data_x, self.x_sampled, self.y_sampled)
        else:
            raise ValueError("Invalid reconstruction method. Choose 'shannon' or 'lanczos'.")

        second_plot_widget.plot(self.data_x, self.y_reconstructed, pen=(50, 100, 240))

    def plot_difference(self, third_plot_widget):
        difference_y = self.data_y - self.y_reconstructed
        third_plot_widget.plot(self.data_x, difference_y, pen=(200, 50, 50))
    def create_frequency_domain(self, plot_widget_frequency_domain):
        # cal freq domain using fft
        self.frequencies = np.fft.fftfreq(len(self.data_y), d=(self.data_x[1] - self.data_x[0]))
        self.amplitude = np.abs(np.fft.fft(self.data_y))
        # self.frequencies = np.fft.fftfreq(len(self.y_reconstructed), d=(self.x_sampled[1] - self.x_sampled[0]))
        # self.amplitude = np.abs(np.fft.fft(self.y_reconstructed))
        print(f"Frequencies: {self.frequencies}")
        print(f"Amplitude: {self.amplitude}")
        # plot the frequency domain signal
        self.frequency_line = plot_widget_frequency_domain.plot(
            self.frequencies,
            self.amplitude,
            pen=pg.mkPen(color = "green", width=2.5),
        )
        self.after_band_width_line = plot_widget_frequency_domain.plot(
            self.frequencies + self.sampling_frequency , self.amplitude , pen =pg.mkPen(color = "red")
        )
        self.before_band_width_line = plot_widget_frequency_domain.plot(
            self.frequencies - self.sampling_frequency , self.amplitude , pen = pg.mkPen(color = "red")
        )

# Application code here (e.g., PyQt setup and UI components, if needed)

