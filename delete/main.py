# import sys
# import pandas as pd
# import numpy as np
# import scipy
# from MainWindowTemp import MainWindow
# from SignalClass import SignalClass, whittaker_shannon_interpolation
# from PyQt5.QtWidgets import QFileDialog, QApplication
#
#
# signals_list = []
# chosen_signal = None
#
#
# def plot_original_signal(data_x, data_y, amplitude, first_plot, color, signal_id):
#     signal = SignalClass(data_x, data_y,'original', amplitude, first_plot, color, len(signals_list) + 1, signal_id)
#     chosen_signal = signal
#     signals_list.append(signal)
#
#
# def plot_reconstructed_signal(data_x, data_y, sampling_period, second_plot):
#     x_sampled = np.arange(np.min(data_x), np.max(data_x), sampling_period)
#     y_sampled = np.interp(x_sampled, data_x, data_y)
#     # reconstructed_signal = reconstructed_signal_class(x_sampled, y_sampled, 'reconstructed')
#     # recovered_y, recovered_x = scipy.signal.resample(x_sampled)
#     y_reconstructed = whittaker_shannon_interpolation(data_x, x_sampled, y_sampled, sampling_period)
#     second_plot.plot(data_x, y_reconstructed, pen='r')
#
#
# # def change_amplitude():
# #     if chosen_signal:
# #         amplitude = 5 # el value el hatla3
# #         chosen_signal.update_amplitude(amplitude)
#
#
#
#
#
