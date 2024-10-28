import sys

import pandas as pd
import scipy.signal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from pyqtgraph import ScatterPlotItem
from scipy.interpolate import interp1d


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sampling Studio')
        self.setGeometry(0, 100, 2500, 1300)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.first_plot_widget = pg.PlotWidget()
        self.second_plot_widget = pg.PlotWidget()
        layout.addWidget(self.first_plot_widget)
        layout.addWidget(self.second_plot_widget)

        # self.third_plot = pg.PlotWidget()
        # self.fourth_plot = pg.PlotWidget()
        # layout.addWidget(self.third_plot)
        # layout.addWidget(self.fourth_plot)

        # # Random Data
        # np.random.seed(5)
        # x = np.linspace(0, 10, 100)
        # y = np.sin(x) + np.random.normal(0, 0.1, 100)
        # self.first_plot_widget.plot(x, y, pen='b')
        #
        # sampling_rate = 100
        # sample_indices = np.linspace(0, len(x) - 1, sampling_rate).astype(int)
        # x_sampled = x[sample_indices]
        # y_sampled = y[sample_indices]
        # self.second_plot_widget.plot(x_sampled, y_sampled, pen='r')
        self.plot_original()
        self.show()

    def shannon_whittaker_reconstruction(self, sampled_y, sampled_x, reconstruction_points):
        sinc_matrix = np.tile(reconstruction_points, (len(sampled_x), 1)) - np.tile(sampled_x[:, np.newaxis],
                                                                                    (1, len(reconstruction_points)))
        return np.dot(sampled_y, np.sinc(sinc_matrix / (sampled_x[1] - sampled_x[0])))

    def plot_original(self):
        ecg_data = pd.read_csv('ECG_DATA.csv')
        self.signal_x = np.array(ecg_data['time'])
        self.signal_y = np.array(ecg_data['signal'])
        self.first_plot_widget.plot(self.signal_x, self.signal_y, pen='r')

        sampling_frequency = 500
        sampling_period = 1 / sampling_frequency

        total_duration = self.signal_x[-1]  # end of time
        reconstruction_points = np.arange(0, total_duration, sampling_period)
        # reconstructed_signal = self.shannon_whittaker_reconstruction()
        # self.plot_reconstructed_signal(sampling_frequency)
        # x_sampled = np.arange(np.min(signal_x), np.max(signal_y), sampling_period)
        # sampling_points = np.arange(np.min(signal_y), np.max(signal_y), sampling_period)
        # self.x_sampled = np.arange(np.min(self.signal_x), np.max(self.signal_x), sampling_period)
        # self.y_sampled = self.sinc_interp(self.signal_y, self.signal_x, self.x_sampled)
        # self.samples = np.interp(self.x_sampled, self.signal_x, self.signal_y)
        # self.first_plot_widget.plot(self.x_sampled, self.samples, pen=None, symbol='o', symbolSize=5, symbolBrush='w')
        # self.second_plot_widget.plot(self.x_sampled, self.y_sampled, pen='b')

        # Interpolate the signal to create a more densely sampled version
        # interp_func = interp1d(signal_x, signal_y, kind='linear')
        # time_sampled = np.arange(signal_x[0], signal_x[-1], 1 / num_samples)
        #
        # sampled_signal = interp_func(time_sampled)
        #
        # sampled_scatter = ScatterPlotItem()
        # sampled_scatter.setData(time_sampled, sampled_signal, symbol='o', brush=(255, 0, 0), size=10)
        # self.second_plot_widget.addItem(sampled_scatter)

        # self.plot_reconstructed(signal, time_sampled, sampled_signal)

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

    def plot_reconstructed_signal(self, sampling_frequency):
        # Downsample the original signal to the given sampling frequency
        sample_interval = 1 / sampling_frequency
        sampled_indices = np.arange(0, len(self.signal_x),
                                    int(sample_interval * len(self.signal_x) / (self.signal_x[-1] - self.signal_x[0])))
        sampled_x = self.signal_x[sampled_indices]
        sampled_y = self.signal_y[sampled_indices]

        # Reconstruct the signal
        reconstructed_signal = self.shannon_whittaker_reconstruction(sampled_y, sampled_x, self.reconstruction_points)

        # Create a plot for this sampling frequency
        self.second_plot_widget = pg.PlotWidget(title=f"Reconstructed Signal at {sampling_frequency} Hz")
        self.second_plot_widget.plot(self.reconstruction_points, reconstructed_signal, pen='r',
                                     name=f"Reconstructed at {sampling_frequency} Hz")
        self.reconstructed_signals.append((sampling_frequency, reconstructed_signal))

    def reconstruct_signal(self):
        recovered_y, recovered_x = scipy.signal.resample(self.x_sampled)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
