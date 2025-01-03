# import sys
#
# import pandas as pd
# import scipy.signal
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# import pyqtgraph as pg
# import numpy as np
# from pyqtgraph import ScatterPlotItem
# from scipy.interpolate import interp1d
# from scipy import special  # For sinc function
#
#     def plot_original(self):
#         # Load original ECG data
#         ecg_data = pd.read_csv('Signals/ECG_DATA.csv')
#         signal_x = np.array(ecg_data['time'])
#         self.signal_y = np.array(ecg_data['signal'])
#
#         # Plot the original signal
#         self.first_plot_widget.plot(signal_x, self.signal_y, pen='b')
#
#         # Sampling parameters
#         sampling_frequency = 250
#         sampling_period = 1 / sampling_frequency
#         self.x_sampled = np.arange(np.min(signal_x), np.max(signal_x), sampling_period)
#
#         # Sampled signal using interpolation
#         self.y_sampled = np.interp(self.x_sampled, signal_x, self.signal_y)
#
#         # Plot the sampled points on the first plot widget
#         self.first_plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=5, symbolBrush='w')
#
#         # Plot the reconstructed sampled signal on the second plot widget
#         # self.second_plot_widget.plot(self.x_sampled, self.y_sampled, pen='g')
#
#         # Reconstruct signal on original `signal_x` using Whittaker-Shannon interpolation
#         def whittaker_shannon_interpolation(x_points, sampled_x, sampled_y):
#             sinc_matrix = np.tile(x_points, (len(sampled_x), 1)) - np.tile(sampled_x[:, None], (1, len(x_points)))
#             reconstructed = np.dot(sampled_y, np.sinc(sinc_matrix / sampling_period))
#             return reconstructed
#
#         self.y_reconstructed = whittaker_shannon_interpolation(signal_x, self.x_sampled, self.y_sampled)
#
#         # Calculate and plot the difference on the third plot widget
#         difference = self.signal_y - self.y_reconstructed
#         self.second_plot_widget.plot(signal_x, self.y_reconstructed, pen='r')
#         self.third_plot_widget.plot(signal_x, difference, pen='r')
#
#
#     # def reconstruct_signal(self, signal, time_sampled, sampled_signal):
#     #     time_domain = np.linspace(0, signal.x[-1], len(signal.x))
#     #     # Creating a 2D matrix with len(time_sampled) rows and len(time_domain) coloumns
#     #     resizing = np.resize(time_domain, (len(time_sampled), len(time_domain)))
#     #     Fs = 1 / (time_sampled[1] - time_sampled[0])
#     #     # Subtract the sample time within the time domain from the 2 columns
#     #     pre_interpolation = (resizing.T - time_sampled) * Fs
#     #     '''Get the sinc value for each value in the resizing matrix so within 0 the value will be 1 and for large
#     #     values it will be zero then multiply these values with its real amplitudes'''
#     #     interpolation = sampled_signal * np.sinc(pre_interpolation)
#     #
#     #     # x(t)=∑ n=−∞ ---> ∞ [x[n]⋅sinc(fs * (t-nTs))
#     #     # t ---> time domain
#     #     # X[n] ---> samples
#     #     # Ts ---> 1/fs
#     #
#     #     # Get the sum of the columns within one column only with the required data
#     #     samples_of_amplitude_at_time_domain = np.sum(interpolation, axis=1)
#     #
#     #     return time_domain, samples_of_amplitude_at_time_domain
#
#         def reconstruct_signal(self):
#             recovered_y, recovered_x = scipy.signal.resample(self.x_sampled)
#
#
#
#
