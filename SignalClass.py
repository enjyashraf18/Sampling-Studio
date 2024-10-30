import numpy as np
from scipy.interpolate import CubicSpline
import pyqtgraph as pg
from composer import SignalComposer



def whittaker_shannon_interpolation(sampled_x, sampled_y, reconstructed_time):
    interval_time = sampled_x[1] - sampled_x[0]
    reconstructed_y = np.array([np.sum(sampled_y * np.sinc((t - sampled_x) / interval_time))
                                for t in reconstructed_time])
    return reconstructed_y


def cubic_spline_interpolation(x_points,sampled_x, sampled_y):
    cs_func = CubicSpline(sampled_x, sampled_y)
    reconstructed_y = cs_func(x_points)
    return reconstructed_y


def lanczos_interpolation(x_points, sampled_x, sampled_y, a=3):
    def lanczos_kernel(x, a):
        if x == 0:
            return 1
        elif -a < x < a:
            return a * np.sin(np.pi * x) * np.sin(np.pi * x / a) / (np.pi ** 2 * x ** 2)
        else:
            return 0

    # initialise to fill
    reconstructed_y = np.zeros_like(x_points)

    for i, t in enumerate(x_points):
        # Sum contributions from all sampled points, weighted by the Lanczos kernel
        for j, t_j in enumerate(sampled_x):
            x = (t - t_j) / (sampled_x[1] - sampled_x[0])  # Relative distance
            reconstructed_y[i] += sampled_y[j] * lanczos_kernel(x, a)
    return reconstructed_y


class SignalClass:
    def __init__(self, data_x, data_y, signal_type, plot_widget, color, signal_id, name):
        self.data_x = data_x
        self.data_y = data_y
        self.type = signal_type  # original, reconstructed, difference, composed
        self.plot_widget = plot_widget
        self.color = color
        self.signal_id = signal_id
        self.maximum_frequency = None
        self.sampling_frequency = None
        self.sampling_period = None
        self.x_sampled = None
        self.y_sampled = None
        self.y_reconstructed = None
        self.start_time = None
        self.end_time = None
        self.frequencies = None
        self.amplitude = None
        self.before_band_width_line = None
        self.after_band_width_line = None
        self.frequency_line = None
        self.snr = None
        self.noisy_data_y = self.data_y
        self.current_snr_CheckBox = False
        self.current_snr_value = 0
        self.current_frequency = self.maximum_frequency
        self.current_reconstruction_method = "shannon"
        self.current_amplitude = 0
        self.current_normalize_checkbox = False
        self.name = name

    def calculate_maximum_frequency(self):
        if self.type != 'composed':
            time = np.array(self.data_x)
            magnitude = np.array(self.noisy_data_y)
            fft_result = np.fft.fft(magnitude)  # time domain to freq domain
            frequencies = np.fft.fftfreq(len(fft_result), time[1] - time[0])
            positive_frequencies = frequencies[frequencies >= 0]
            self.maximum_frequency = positive_frequencies[-1]
            print(f"hena fmax composed {self.maximum_frequency}")
            self.sampling_frequency = 2*self.maximum_frequency
            print(f"SAMPLING FREQUENCY: {self.sampling_frequency}")
            self.sampling_period = 1/self.sampling_frequency

    def plot_original_signal(self):
        self.plot_widget.plot(self.data_x, self.noisy_data_y, pen=self.color)

    def plot_sample_points(self):
        self.start_time = np.min(self.data_x)
        self.end_time = np.max(self.data_x)
        self.x_sampled = np.arange(self.start_time, self.end_time, self.sampling_period)
        self.y_sampled = np.interp(self.x_sampled, self.data_x, self.noisy_data_y)
        # for x, y in zip(self.data_x, self.data_y):
        #     if x in x_sampled:
        #         y_sampled.append(y)
        self.plot_widget.plot(self.x_sampled, self.y_sampled, pen=None, symbol='o', symbolSize=4, symbolBrush='w')

    def plot_reconstructed_signal(self, second_plot_widget, method):
        reconstructed_time = np.linspace(self.start_time, self.end_time, 1000)

        if method == 'Whittaker-Shannon':
            print("Reconstruction Method: Whittaker-Shannon")
            self.y_reconstructed = whittaker_shannon_interpolation(self.x_sampled, self.y_sampled, reconstructed_time)
        elif method == 'Lanczos':
            print("Reconstruction Method: Lanczos")
            self.y_reconstructed = lanczos_interpolation(reconstructed_time, self.x_sampled, self.y_sampled, a=3)
        elif method == 'Cubic Spline':
            print("Reconstruction Method: Cubic Spline")
            self.y_reconstructed = cubic_spline_interpolation(reconstructed_time, self.x_sampled, self.y_sampled)
        else:
            raise ValueError("Invalid reconstruction method. Choose 'Whittaker-Shannon', 'Lanczos', or 'Cubic Spline'.")

        # Plot the reconstructed signal
        second_plot_widget.plot(reconstructed_time, self.y_reconstructed, pen=(50,100,240))

    def plot_difference(self, third_plot_widget):
        difference_y = self.noisy_data_y - self.y_reconstructed
        min_y = min(difference_y)
        max_y = max(difference_y)
        # third_plot_widget.getPlotItem().autoRange()
        third_plot_widget.setLimits(xMin=min(self.data_x), xMax=max(self.data_x), yMin=min_y, yMax=max_y)
        third_plot_widget.plot(self.data_x, difference_y, pen=(200,50,50))

    def create_frequency_domain(self, plot_widget_frequency_domain):
        # cal freq domain using fft
        self.frequencies = np.fft.fftfreq(len(self.data_y), d=(self.data_x[1] - self.data_x[0]))
        self.amplitude = np.abs(np.fft.fft(self.data_y))
        # self.frequencies = np.fft.fftfreq(len(self.y_reconstructed), d=(self.x_sampled[1] - self.x_sampled[0]))
        # self.amplitude = np.abs(np.fft.fft(self.y_reconstructed))
        # print(f"Frequencies: {self.frequencies}")
        # print(f"Amplitude: {self.amplitude}")
        # plot the frequency domain signal
        self.frequency_line = plot_widget_frequency_domain.plot(
            self.frequencies,
            self.amplitude,
            pen=pg.mkPen(color="green", width=2.5),
        )
        self.after_band_width_line = plot_widget_frequency_domain.plot(
            self.frequencies + self.sampling_frequency, self.amplitude, pen=pg.mkPen(color="red")
        )
        self.before_band_width_line = plot_widget_frequency_domain.plot(
            self.frequencies - self.sampling_frequency , self.amplitude , pen = pg.mkPen(color = "red")
        )
    def adding_noise(self):
        snr_db = float(self.snr)
        # snr range from -10 to 50 dB
        # Calculate signal power as the mean square of the signal
        signal_power = np.mean(self.data_y ** 2)

        # Calculate noise power based on desired SNR
        snr_linear = 10 ** (snr_db / 10)  # Convert dB to linear scale
        noise_power = signal_power / snr_linear

        # Generate Gaussian noise and scale it to match the desired noise power
        noise = np.random.normal(0, np.sqrt(noise_power), self.data_y.shape)

        # Create the noisy signal by adding noise to the y-axis values
        self.noisy_data_y = self.data_y + noise

        # return noisy_y

    def update_data(self, data_x, data_y, max_freq):
        self.data_x = data_x
        self.data_y = data_y
        self.maximum_frequency = max_freq
        self.sampling_frequency = 2*self.maximum_frequency
        self.sampling_period = 1 / self.sampling_frequency
    
    def remove_noise(self):
        self.noisy_data_y = self.data_y




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


