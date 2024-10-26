import sys
import pandas as pd
import numpy as np
import scipy
from MainWindowTemp import MainWindow
from Signal import Signal, whittaker_shannon_interpolation
from PyQt5.QtWidgets import QFileDialog, QApplication


def plot_original_signal(data_x, data_y, first_plot):
    original_signal = Signal(data_x, data_y, 'original')
    # original_signal.color = QColor(100, 25, 140)
    first_plot.plot(original_signal.x, original_signal.y, pen=(100, 25, 140))


def plot_reconstructed_signal(data_x, data_y, sampling_period, second_plot):
    x_sampled = np.arange(np.min(data_x), np.max(data_x), sampling_period)
    y_sampled = np.interp(x_sampled, data_x, data_y)
    reconstructed_signal = Signal(x_sampled, y_sampled, 'reconstructed')
    # recovered_y, recovered_x = scipy.signal.resample(x_sampled)
    y_reconstructed = whittaker_shannon_interpolation(data_x, x_sampled, y_sampled, sampling_period)
    second_plot.plot(data_x, y_reconstructed, pen='r')





